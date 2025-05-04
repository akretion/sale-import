# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from datetime import timedelta

from odoo import _, fields, models
from odoo.exceptions import ValidationError

from ..utils import load_purchase_order_pages


class SaleChannel(models.Model):
    _name = "sale.channel"
    _inherit = ["sale.channel", "server.env.mixin"]

    channel_type = fields.Selection(selection_add=[("amazon_vendor", "Amazon Vendor")])

    date_filter_type = fields.Selection(
        [
            ("createdAfter", "Date Created After"),
            ("changedAfter", "Date Changed After"),
        ],
        help="Specifies which date filter to apply when retrieving Amazon orders. "
        "Choose 'Date Changed After' to get orders modified since a specific date, "
        "or 'Date Created After' to get orders placed since a specific date.",
    )
    date_filter = fields.Datetime(
        help="The reference date used to filter Amazon orders based on the "
        "selected date filter type. Only orders created or modified after this date "
        "(depending on your selection) will be retrieved from Amazon.",
        default=lambda self: fields.Datetime.now() - timedelta(days=30),
    )

    def amazon_vendor_import_orders(self):
        if self.channel_type != "amazon_vendor":
            raise ValidationError(_("The sale channel must be type 'Amazon Vendor'"))
        if not self.date_filter_type:
            raise ValidationError(_("Missing Date Filtering Type"))
        if not self.date_filter:
            raise ValidationError(_("Missing Date Filtering"))

        orders = []
        creds = self.amazon_get_credentials()
        date_filter = self.date_filter.isoformat(sep="T")

        for marketplace_id in self.marketplace_ids:
            country_code = marketplace_id.country_code
            pages = load_purchase_order_pages(
                creds, country_code, self.date_filter_type, date_filter
            )
            for page in pages:
                orders.extend([order for order in page.payload.get("orders")])

        return orders

    def amazon_vendor_import_orders_chunk(self):
        self.ensure_one()
        orders = self.amazon_vendor_import_orders()
        chunk_vals = [
            {
                "data_str": json.dumps(order, indent=4),
                "processor": "sale_channel_importer_amazon_vendor",
                "model_name": "sale.channel",
                "record_id": self.id,
            }
            for order in orders
        ]
        chunk_ids = self.env["queue.job.chunk"].sudo().create(chunk_vals)
        self.write({"date_filter": fields.Datetime.now()})
        return chunk_ids

    def amazon_vendor_import_orders_chunk_cron(self):
        amazon_channel_ids = self.search([("channel_type", "=", "amazon_vendor")])
        chunk_ids = self.env["queue.job.chunk"]
        for channel_id in amazon_channel_ids:
            new_chunk_ids = channel_id.amazon_vendor_import_orders_chunk()
            chunk_ids |= new_chunk_ids

        return chunk_ids
