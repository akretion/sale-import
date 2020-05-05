# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests import TransactionCase


class TestSaleChannel(TransactionCase):
    def setUp(self):
        super().setUp()
        self.sale_channel = self.env["sale.channel"].create(
            {"name": "some sale channel"}
        )
        self.partner = self.env.ref("base.res_partner_12")
        self.product = self.env.ref("product.product_product_4")
        self.product.invoice_policy = "order"

    def test_sale_channel(self):
        so_vals = {
            "name": "SO XYZ",
            "partner_id": self.partner.id,
            "sale_channel_id": self.sale_channel.id,
        }
        sale_order = self.env["sale.order"].create(so_vals)
        so_line_vals = {
            "name": "description",
            "price_unit": 3.3,
            "product_uom_qty": 5.5,
            "product_id": self.product.id,
            "order_id": sale_order.id,
        }
        self.env["sale.order.line"].create(so_line_vals)
        sale_order.action_confirm()
        sale_order.action_invoice_create()
        binding = self.env["res.partner.binding"].search(
            [("partner_id", "=", self.partner.id)]
        )
        self.assertTrue(binding.partner_id == self.partner)
        self.assertTrue(binding.sale_channel_id == self.sale_channel)

    def test_api_key_recognized(self):  # todo
        pass

    def test_api_key_wrong(self):
        pass
