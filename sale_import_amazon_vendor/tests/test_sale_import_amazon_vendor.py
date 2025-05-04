# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta
from unittest.mock import patch

from odoo import fields
from odoo.tests import TransactionCase, tagged

from odoo.addons.sale_import_amazon_vendor.tests import data

PATCH = (
    "odoo.addons.sale_import_amazon_vendor.models.sale_channel.SaleChannel"
    ".amazon_vendor_import_orders"
)


@tagged("-at_install", "post_install")
class TestSaleImportAmazonVendor(TransactionCase):
    def setUp(self):
        super().setUp()
        self.env = self.env(
            context=dict(self.env.context, test_queue_job_no_delay=True)
        )
        self.tax_incl = self.env["account.tax"].create(
            {
                "name": "Test Tax Include",
                "amount": "10",
                "price_include": True,
                "type_tax_use": "sale",
            }
        )
        self.product = self.env["product.product"].create(
            {
                "name": "Product",
                "default_code": "PROD_1",
                "invoice_policy": "order",
                "taxes_id": [(6, 0, [self.tax_incl.id])],
            }
        )
        self.marketplace_id = self.env.ref("sale_import_amazon_base.marketplace_FR")
        self.team_id = self.env["crm.team"].create({"name": "Test"})
        self.pricelist_id = self.env["product.pricelist"].create(
            {"name": "Test EUR", "currency_id": 1}
        )
        self.channel_id = self.env["sale.channel"].create(
            {
                "name": "Amazon",
                "channel_type": "amazon_vendor",
                "marketplace_ids": [(6, 0, [self.marketplace_id.id])],
                "date_filter_type": "changedAfter",
                "date_filter": fields.Datetime.now() - timedelta(days=2),
                "crm_team_id": self.team_id.id,
                "sale_orders_check_amounts_total": True,
                "confirm_order": False,
                "invoice_order": False,
                "pricelist_id": self.pricelist_id.id,
            }
        )
        self.amazon1 = self.env["res.partner"].create({"name": "Amazon 1"})
        self.env["sale.channel.partner"].create(
            [
                {
                    "sale_channel_id": self.channel_id.id,
                    "partner_id": self.amazon1.id,
                    "external_id": "AMZ1",
                }
            ]
        )

    # def test_create_queue_job_chunk(self):
    #     chunk_ids = self.env["sale.channel"].amazon_vendor_import_orders_chunk_cron()
    #     self.assertTrue(chunk_ids)
    #     for chunk_id in chunk_ids:
    #         self.assertIn("purchaseOrderNumber", chunk_id.data_str)
    #         self.assertEqual(chunk_id.processor, "sale_channel_importer_amazon_vendor")

    def test_import_order_new(self):
        with patch(PATCH, return_value=data.ORDER_NEW):
            old_order_ids = self.env["sale.order"].search([])
            self.channel_id.amazon_vendor_import_orders_chunk()

            order = self.env["sale.order"].search([]) - old_order_ids

            self.assertEqual(order.name, "712YDSMD")
            self.assertEqual(order.amount_total, 25)
            self.assertEqual(order.si_amount_total, 25)
            self.assertEqual(order.currency_id.name, "EUR")
            self.assertEqual(order.team_id, self.team_id)
            self.assertEqual(order.state, "draft")
            self.assertEqual(order.partner_id, self.amazon1)

            line = order.order_line
            self.assertEqual(line.name, "ASIN: AMZ_PROD_1")
            self.assertEqual(line.price_unit, 12.5)
            self.assertEqual(line.product_uom_qty, 2)
            self.assertEqual(line.product_id.default_code, "PROD_1")

    # def test_import_order_acknowledged(self):
    #     pass

    # def test_import_order_closed(self):
    #     pass
