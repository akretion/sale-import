# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_compare


class ProductProductChannel(models.Model):
    _name = "channel.product.product"
    _inherit = ["channel.product.product", "sale.channel.hook.mixin"]

    last_notification_qty = fields.Float(
        help="Stock quantity " "when the last notification was sent"
    )

    def _notify_stock_variation(self):
        self.ensure_one()
        current_stock = self.record_id.with_context(
            warehouse=self.channel_id.warehouse_id
        ).qty_available
        if float_compare(self.last_notification_qty, current_stock) != 0:
            self.last_notification_qty = current_stock
            self.trigger_channel_hook(
                "stock_variation",
                {"product_id": self.record_id.id, "amount": current_stock},
            )

    def get_hook_content_stock_variation(self, data):
        return {"name": "stock_variation", "data": data}
