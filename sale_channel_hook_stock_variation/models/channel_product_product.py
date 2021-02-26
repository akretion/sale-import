# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_compare


class ProductProductChannel(models.Model):
    _inherit = "channel.product.product"

    last_notification_qty = fields.Float(
        help="Stock quantity " "when the last notification was sent"
    )

    def _prepare_qty_variation(self):
        self.ensure_one()
        current_stock = self.record_id.property_stock_inventory
        if float_compare(self.last_notification_qty, current_stock) != 0:
            self.last_notification_qty = current_stock
            return current_stock
