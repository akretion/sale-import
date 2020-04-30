# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.sale.tests.test_sale_common import TestCommonSaleNoChart


class TestSaleChannel(TestCommonSaleNoChart):
    def setUp(self):
        super().setUp()
        self.sale_channel = self.env.ref("sale_channel.sale_channel_amazon")
        self.sale_order = self.env.ref("sale.sale_order_3")
        self.partner = self.env.ref("base.res_partner_4")

    def test_sale_channel(self):
        self.sale_order.sale_channel_id = self.sale_channel
        self.sale_order.order_line.mapped("product_id").write(
            {"invoice_policy": "order"}
        )
        self.sale_order.action_confirm()
        generated_invoice_ids = self.sale_order.action_invoice_create()
        generated_invoices = self.env["account.invoice"].browse(generated_invoice_ids)
        for invoice in generated_invoices:
            self.assertTrue(invoice.sale_channel_id.id == self.sale_channel.id)
