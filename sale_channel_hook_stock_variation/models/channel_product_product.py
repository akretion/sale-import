# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_compare


class ProductProductChannel(models.Model):
    _inherit = "channel.product.product"

    sale_channel_id = fields.Many2one("sale.channel")
    last_notification_qty = fields.Float(
        help="Stock quantity " "when the last notification was sent"
    )

    def _prepare_qty_variations(self):
        result = {}
        for rec in self:
            current_stock = rec.record_id.property_stock_inventory
            if float_compare(rec.last_notification_qty, current_stock) != 0:
                result[rec.record_id.id] = current_stock
                rec.last_notification_qty = current_stock
        return result
