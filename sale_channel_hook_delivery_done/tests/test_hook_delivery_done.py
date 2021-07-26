#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tests.common import SavepointCase


class TestHookSaleDeliveryDone(SavepointCase):
    def _get_picking_content(self):
        self.sale.action_confirm()
        for el in self.sale.picking_ids:
            el.action_confirm()
        picking_ship = self.sale.picking_ids.filtered(
            lambda r: r.picking_type_id == self.env.ref("stock.picking_type_out")
        )
        picking_pick = self.sale.picking_ids - picking_ship
        picking_pick.move_lines.quantity_done = 1.00
        picking_pick.action_put_in_pack()
        picking_pick.button_validate()
        picking_ship.move_lines.quantity_done = 1.00
        picking_ship.button_validate()
        content = picking_ship.get_hook_content_delivery_done()["data"]
        return (content, picking_ship)

    def setUp(self):
        super().setUp()
        self.env.ref("stock.warehouse0").delivery_steps = "pick_ship"
        self.channel = self.env.ref("sale_channel.sale_channel_amazon")
        self.channel.hook_active_delivery_done = True
        self.channel.hook_picking_type_ids = [
            (6, False, [self.env.ref("stock.picking_type_out").id])
        ]
        self.sale = self.env["sale.order"].create(
            {
                "partner_id": self.env.ref("base.res_partner_3").id,
                "sale_channel_id": self.channel.id,
                "carrier_id": self.env.ref("delivery.normal_delivery_carrier").id,
            }
        )
        self.env["sale.order.line"].create(
            {
                "product_id": self.env.ref("product.product_product_25").id,
                "name": "someDesc",
                "product_uom_qty": 1,
                "order_id": self.sale.id,
            }
        )
        self.sale.action_confirm()
        for sol in self.sale.order_line:
            sol.product_id.invoice_policy = "order"

    def test_hook_delivery_done(self):
        """
        Create SO, mark pickings as delivered
        """
        content, picking_ship = self._get_picking_content()
        self.assertEqual(content["sale_name"], self.sale.client_order_ref)
        self.assertEqual(content["picking"], picking_ship.name)
        self.assertEqual(content["carrier"], "Normal Delivery Charges")
        expected_tracking = [{"number": picking_ship.package_ids.name}]
        self.assertEqual(content["tracking"], expected_tracking)
