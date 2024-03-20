# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import os
from datetime import timedelta
from unittest.mock import patch

from odoo import Command, fields
from odoo.tests import TransactionCase

from odoo.addons.extendable.tests.common import ExtendableMixin
from odoo.addons.sale_import_amazon.tests import data


class TestConnectorAmazon(TransactionCase, ExtendableMixin):
    @classmethod
    def setUpClass(cls):
        super(TestConnectorAmazon, cls).setUpClass()
        cls.init_extendable_registry()

    def setUp(self):
        super().setUp()
        self.env = self.env(
            context=dict(self.env.context, test_queue_job_no_delay=True)
        )
        original_tax = self.env.ref("l10n_generic_coa.1_purchase_tax_template")
        self.tax_incl = original_tax.copy({"price_include": True})
        self.product = self.env["product.product"].create(
            {
                "name": "Product",
                "default_code": "PROD_1",
                "invoice_policy": "order",
                "taxes_id": [Command.set([self.tax_incl.id])],
            }
        )
        self.marketplace_id = self.env.ref("sale_import_amazon.marketplace_FR")
        self.team_id = self.env["crm.team"].create({"name": "Test"})
        self.pricelist_id = self.env["product.pricelist"].create(
            {"name": "Test EUR", "currency_id": 1}
        )
        self.channel_id = self.env["sale.channel"].create(
            {
                "name": "Connector Odoo-Amazon",
                "channel_type": "amazon",
                "lwa_appid": os.environ.get("LWA_APP_ID"),
                "sp_api_refresh_token": os.environ.get("SP_API_REFRESH_TOKEN"),
                "lwa_client_secret": os.environ.get("LWA_CLIENT_SECRET"),
                "marketplace_ids": [Command.set([self.marketplace_id.id])],
                "date_last_sale_update": fields.Datetime.now() - timedelta(days=60),
                "crm_team_id": self.team_id.id,
                "sale_orders_check_amounts_total": True,
                "confirm_order": True,
                "invoice_order": True,
                "pricelist_id": self.pricelist_id.id,
            }
        )

    def test_create_queue_job_chunk(self):
        chunk_ids = self.env["sale.channel"].amazon_import_orders_chunk_cron()
        self.assertTrue(chunk_ids)
        for chunk_id in chunk_ids:
            self.assertIn("AmazonOrderId", chunk_id.data_str)
            self.assertEqual(chunk_id.processor, "sale_channel_importer_amazon")

    def test_import_order_shipped(self):
        with patch(
            "odoo.addons.sale_import_amazon.models.sale_channel.SaleChannel"
            ".amazon_import_orders",
            return_value=data.ORDER_SHIPPED,
        ):
            old_order_ids = self.env["sale.order"].search([])
            self.channel_id.amazon_import_orders_chunk()

            order = self.env["sale.order"].search([]) - old_order_ids

            self.assertEqual(order.name, "407-6462826-9892326")
            self.assertEqual(order.amount_total, 95.98)
            self.assertEqual(order.si_amount_total, 95.98)
            # TODO: how to test the date_order value before confirmation ?
            # self.assertEqual(order.date_order, datetime.datetime(2024, 1, 11))
            self.assertEqual(order.currency_id.id, 1)
            self.assertTrue(order.is_fulfilled_by_amazon)
            self.assertEqual(order.team_id, self.team_id)
            self.assertEqual(order.amazon_marketplace_id, self.marketplace_id)
            self.assertEqual(order.state, "sale")
            # TODO
            # self.assertEqual(order.delivery_status, "full")
            # self.assertEqual(order.state, "done")

            partner = order.partner_id
            self.assertEqual(partner.name, "Amazon Customer #407-6462826-9892326")
            self.assertEqual(partner.city, "Nanterre")
            self.assertEqual(partner.zip, "92000")
            self.assertEqual(partner.country_id.code, "FR")
            self.assertEqual(
                partner.sale_channel_partner_ids.external_id,
                "0fqqxc7r722f7fk@marketplace.amazon.fr",
            )

            line = order.order_line
            self.assertEqual(line.name, "Clever Elf - Décoration de Table de Noël")
            self.assertEqual(line.discount, 0)
            self.assertEqual(line.price_unit, 47.99)
            self.assertEqual(line.product_uom_qty, 2)
            self.assertEqual(line.product_id.default_code, "PROD_1")

    def test_import_order_canceled(self):
        pass

    def test_import_existing_order_to_cancel(self):
        pass

    def test_import_existing_order_to_ship(self):
        pass
