# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.queue_job.job import identity_exact

_logger = logging.getLogger(__name__)


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    product_stock_field_id = fields.Many2one(
        "ir.model.fields",
        "Product stock field",
        domain=[
            ("ttype", "in", ["float", "integer"]),
            ("model", "in", ["product.product", "product.template"]),
        ],
        help="Field used to store the current stock of a product.product",
        default=lambda self: self._default_stock_field_id(),
    )

    def _default_stock_field_id(self):
        return self.env.ref("stock.field_product_product__free_qty")

    hook_active_stock_variation = fields.Boolean("Active stock variation hook")
    warehouse_id = fields.Many2one("stock.warehouse")
    get_stock_info_url = fields.Char(
        "Stock API endpoint URL",
        help="The url of api endpoint who give the stock value",
        default="https://exemple.org/get_stock?page={page_num}",
    )
    enable_stock_sync = fields.Boolean(
        "Enable stock synchronisation (check stock in channel endpoint then syncs if delta)"
    )

    def _get_data_stock(self, page):
        url = self.get_stock_info_url
        url = url.replace("{page_num}", str(page)) + "&token=" + self.auth_token
        response = requests.get(url)
        return response.json()

    def sync_stock(self):
        if not self.get_stock_info_url or not self.auth_token:
            raise ValidationError(
                _(
                    "Set a secret token and define an API "
                    "endpoint to use this channel's hook"
                )
            )
        page = 1
        while True:
            data = self._get_data_stock(page)
            page += 1
            if data:
                for line in data:
                    code, qty = line["default_code"], line["quantity"]
                    prd = self.env["product.product"].search(
                        [("default_code", "=", code)]
                    )
                    if prd:
                        for channel in prd.channel_bind_ids:
                            stock_qty = channel.last_notification_qty
                            if stock_qty != qty:
                                prd.channel_bind_ids.with_delay(
                                    identity_key=identity_exact,
                                    description="Force synchronisation du to stock error",
                                )._notify_channel_stock_variation()

                    else:
                        _logger.info(
                            "Synchronisation du stock, produit non référencé dans odoo:  %s "
                            % code
                        )
            else:
                break
