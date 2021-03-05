#  Copyright (c) Akretion 2021
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from mock import patch

from odoo.tests import SavepointCase


class TestHookSaleState(SavepointCase):
    def _set_initial_stock_to(self, qty):
        inventory = self.env["stock.inventory"].create(
            {"location_ids": [self.location.id], "name": "Test starting inventory"}
        )
        self.env["stock.inventory.line"].create(
            {
                "inventory_id": inventory.id,
                "location_id": self.location.id,
                "product_id": self.product.id,
                "product_uom_id": self.product.uom_id.id,
                "product_qty": qty,
            }
        )
        inventory.action_start()
        inventory.action_validate()

    def setUp(self):
        super().setUp()
        self.warehouse = self.env.ref("stock.warehouse0")
        self.warehouse_dst = self.env["stock.warehouse"].create(
            {
                "name": "External warehouse",
                "code": "TEST",
                "lot_stock_id": [
                    6,
                    0,
                    {
                        "name": "Test Location for ext. warehouse",
                    },
                ],
            }
        )
        self.partner = self.env.ref("base.res_partner_4")
        self.product = self.env.ref("product.product_product_4")
        self.product.type = "product"
        self.channel = self.env.ref("sale_channel.sale_channel_amazon")
        self.channel.warehouse_id = self.warehouse
        self.binding_tmpl_id = self.env["channel.product.template"].create(
            {
                "record_id": self.product.product_tmpl_id.id,
                "sale_channel_id": self.channel.id,
            }
        )
        self.binding = self.binding_tmpl_id.channel_variant_ids
        self.location = self.warehouse.lot_stock_id
        self.location_dst = self.warehouse_dst.lot_stock_id
        self._set_initial_stock_to(100.0)
        self.picking = (
            self.env["stock.picking"]
            .create(
                {
                    "name": "Test Picking",
                    "location_id": self.location.id,
                    "location_dest_id": self.location_dst.id,
                    "picking_type_id": self.env.ref("stock.picking_type_out").id,
                    "move_lines": [
                        (
                            0,
                            0,
                            {
                                "name": "Test Move",
                                "product_uom_qty": 3.0,
                                "product_id": self.product.id,
                                "product_uom": self.product.uom_id.id,
                            },
                        )
                    ],
                }
            )
            .with_context(test_queue_job_no_delay=True)
        )

    def test_stock_variation_done(self):
        fn_name = (
            "odoo.addons.sale_channel_hook"
            ".models.sale_channel_hook_mixin"
            ".SaleChannelHookMixin"
            ".trigger_channel_hook"
        )
        self.picking.move_lines.quantity_done = 3.0
        with patch(fn_name) as mock:
            self.picking.button_validate()
            mock.assert_called_with(
                "stock_variation", {"product_id": self.product.id, "amount": 97.0}
            )
