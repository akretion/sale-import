# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from datetime import timedelta

from odoo import _, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.sale_import_amazon.utils import load_order_items, load_order_pages


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    channel_type = fields.Selection(selection_add=[("amazon", "Amazon")])

    lwa_appid = fields.Char(string="LWA App ID")
    # TODO: use data_encryption to store these fields here
    sp_api_refresh_token = fields.Char(string="SP-API Refresh Token")
    lwa_client_secret = fields.Char(string="LWA Client Secret")

    date_last_sale_update = fields.Datetime(
        help="Date used to limit the API call to the last Amazon Orders updated after "
        "this choosen date",
        default=lambda self: fields.Datetime.now() - timedelta(days=30),
    )

    marketplace_ids = fields.Many2many(
        "amazon.marketplace",
        string="MarketPlaces",
        help="List of the MarketPlaces to be sync with Odoo through this backend app",
    )
    amazon_location_id = fields.Many2one(
        "stock.location", string="Amazon Stock Location"
    )

    def amazon_get_credentials(self):
        return dict(
            lwa_app_id=self.lwa_appid,
            refresh_token=self.sp_api_refresh_token,
            lwa_client_secret=self.lwa_client_secret,
        )

    def amazon_import_orders(self):
        if self.channel_type != "amazon":
            raise ValidationError(_("The sale channel must be type 'Amazon'"))

        orders = []
        creds = self.amazon_get_credentials()
        if not self.date_last_sale_update:
            raise ValidationError(_("Missing Date Last Sale Update"))
        date_last_sale_update = self.date_last_sale_update.isoformat(sep="T")

        for marketplace_id in self.marketplace_ids:
            country_code = marketplace_id.country_code
            pages = load_order_pages(creds, country_code, date_last_sale_update)
            for page in pages:
                for order in page.payload.get("Orders"):
                    amazon_ref = order.get("AmazonOrderId")
                    items = load_order_items(creds, country_code, amazon_ref)
                    order.update({"OrderItems": items.payload.get("OrderItems")})
                    orders.append(order)

        return orders

    def amazon_import_orders_chunk(self):
        self.ensure_one()
        orders = self.amazon_import_orders()

        chunk_vals = [
            {
                "data_str": json.dumps(order),
                "processor": "sale_channel_importer_amazon",
                "model_name": "sale.channel",
                "record_id": self.id,
            }
            for order in orders
        ]
        chunk_ids = self.env["queue.job.chunk"].create(chunk_vals)
        self.write({"date_last_sale_update": fields.Datetime.now()})
        return chunk_ids

    def amazon_import_orders_chunk_cron(self):
        amazon_channel_ids = self.search([("channel_type", "=", "amazon")])
        chunk_ids = self.env["queue.job.chunk"]
        for channel_id in amazon_channel_ids:
            new_chunk_ids = channel_id.amazon_import_orders_chunk()
            chunk_ids |= new_chunk_ids

        return chunk_ids
