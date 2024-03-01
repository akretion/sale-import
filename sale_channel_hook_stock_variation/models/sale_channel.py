# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import requests

from odoo import fields, models

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
        url = self.get_stock_info_url.format(page_num=page)
        headers, payload, url = self._apply_webhook_security({}, {}, url)
        response = requests.get(url, headers=headers)
        return response.json()

    def _check_stock_level(self, data):
        for line in data:
            code, qty = line["default_code"], line["quantity"]
            prd = self.env["channel.product.product"].search(
                [
                    ("record_id.default_code", "=", code),
                    ("sale_channel_id", "=", self.id),
                ]
            )
            if prd and prd.last_notification_qty != qty:
                prd.with_delay(
                    identity_key=identity_exact,
                    description="Force synchronisation du to stock error",
                )._notify_channel_stock_variation()

            else:
                _logger.info(
                    "Synchronisation du stock, produit non référencé dans odoo:  %s "
                    % code
                )

    def sync_stock(self):
        page = 1
        while True:
            data = self._get_data_stock(page)
            page += 1
            if data:
                self._check_stock_level(data)
            else:
                break
