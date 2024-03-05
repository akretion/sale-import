# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from pprint import pprint


from odoo import _, api, Command, fields, models
from odoo.exceptions import ValidationError
from odoo.addons.sale_import_amazon.utils import load_order_pages, load_order_items


class SaleChannel(models.Model):
    _inherit = "sale.channel"
    # Connect to API, get raw data and create chunk with raw data and processor == sale_channel_importer_amazon

    type_channel = fields.Selection(selection_add=[("amazon", "Amazon")])

    lwa_appid = fields.Char(string="LWA App ID")
    # TODO: use data_encryption to store these fields here
    sp_api_refresh_token = fields.Char()
    lwa_client_secret = fields.Char()

    date_last_sale_update = fields.Datetime(
        help="Date used to limit the API call to the last Amazon Orders updated after "
        "this choosen date"
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
        self.ensure_one()
        return dict(
            lwa_app_id=self.lwa_appid,
            refresh_token=self.sp_api_refresh_token,
            lwa_client_secret=self.lwa_client_secret,
        )

    def amazon_import_orders(self):
        if self.type_channel != "amazon":
            raise ValidationError(_("The sale channel must be type 'Amazon'"))

        orders = []
        creds = self.amazon_get_credentials()
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

    def amazon_create_queue_job_chunk(self):
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

        return self.env["queue.job.chunk"].create(chunk_vals)
