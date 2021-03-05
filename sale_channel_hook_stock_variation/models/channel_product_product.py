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

    def _get_stock_level(self):
        field_name = self.channel_id.product_stock_field_id.name
        return record.record_id.with_context(warehouse=self.channel_id.warehouse_id)[field_name]
    
    def _check_stock_variation(self):
        for record in self:
            val = self._get_stock_level()
            if float_compare(record.last_notification_qty, val) != 0:
                record.with_delay(identity=identity)._notify_stock_variation()

    def _notify_stock_variantion(self):
        self.ensure_one() 
        val = self._get_stock_level()
        self.last_notification_qty = val
        self.trigger_channel_hook(
            "stock_variation",
            {"product_id": self.record_id.id, "amount": val},
        )
    def get_hook_content_stock_variation(self, data):
        return {"name": "stock_variation", "data": data}
