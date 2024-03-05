# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import os
import datetime


from datetime import timedelta
from unittest.mock import patch

from odoo import fields, Command

from odoo.tests import TransactionCase

from odoo.addons.sale_import_amazon.tests import data
from odoo.addons.sale_import_amazon.utils import get_amz_date

from odoo.addons.extendable.tests.common import ExtendableMixin


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
        self.marketplace_id = self.env["amazon.marketplace"].create(
            {
                "name": "Amazon.fr",
                "country_code": "FR",
                "marketplace_ref": "A13V1IB3VIYZZH",
            }
        )
        self.team_id = self.env["crm.team"].create({"name": "Test"})
        self.channel_id = self.env["sale.channel"].create(
            {
                "name": "Connector Odoo-Amazon",
                "type_channel": "amazon",
                "lwa_appid": os.environ.get("LWA_APP_ID"),
                "sp_api_refresh_token": os.environ.get("SP_API_REFRESH_TOKEN"),
                "lwa_client_secret": os.environ.get("LWA_CLIENT_SECRET"),
                "marketplace_ids": [Command.set([self.marketplace_id.id])],
                "date_last_sale_update": fields.Datetime.now() - timedelta(days=30),
                "crm_team_id": self.team_id.id,
                "sale_orders_check_amounts_total": True,
                "confirm_order": False,
                "invoice_order": False,
            }
        )

    def test_create_queue_job_chunk(self):
        chunk_ids = self.channel_id.amazon_create_queue_job_chunk()
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
            self.channel_id.amazon_create_queue_job_chunk()

            order = self.env["sale.order"].search([]) - old_order_ids

            self.assertEqual(order.name, "407-6462826-9892326")
            self.assertEqual(order.amount_total, 95.98)
            self.assertEqual(order.si_amount_total, 95.98)
            self.assertEqual(order.date_order, datetime.datetime(2024, 1, 11))
            self.assertEqual(order.currency_id.id, 1)
            self.assertTrue(order.is_fulfilled_by_amazon)
            # TODO
            # self.assertEqual(order.state, "done")
            # self.assertEqual(order.delivery_status, "full")

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
            self.assertEqual(line.product_id.default_code, "FURN_8888")

    def test_import_order_canceled(self):
        pass

    def test_import_existing_order_to_cancel(self):
        pass

    def test_import_existing_order_to_ship(self):
        pass
