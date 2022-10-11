# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_compare

from odoo.addons.queue_job.job import identity_exact


class ProductProductChannel(models.Model):
    _name = "channel.product.product"
    _inherit = ["channel.product.product", "sale.channel.hook.mixin"]

    last_notification_qty = fields.Float(
        help="Stock quantity " "when the last notification was sent"
    )

    def _get_stock_level(self):
        field_name = self.sale_channel_id.product_stock_field_id.name
        return self.record_id.with_context(
            warehouse=self.sale_channel_id.warehouse_id.id
        )[field_name]

    def _check_stock_variation(self, force=False):
        for rec in self:
            val = rec._get_stock_level()
            if (
                force
                or float_compare(rec.last_notification_qty, val, precision_digits=2)
                != 0
            ):
                rec.with_delay(
                    identity_key=identity_exact
                )._notify_channel_stock_variation()

    def _notify_channel_stock_variation(self):
        for rec in self:
            val = rec._get_stock_level()
            rec.last_notification_qty = val
            rec.trigger_channel_hook(
                "stock_variation",
                {"product_code": self.record_id.default_code, "qty": val},
            )

    def get_hook_content_stock_variation(self, data):
        return {"name": "stock_variation", "data": data}
