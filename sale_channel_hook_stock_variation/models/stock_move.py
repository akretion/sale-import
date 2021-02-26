# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = ["stock.move", "sale.channel.hook.mixin"]

    def _notify_stock_variation(self):
        for rec in self:
            products_moved = rec.move_line_ids.mapped("product_id")
            warehouse = rec.warehouse_id
            channels = rec.env["sale.channel"].search(
                [
                    ("warehouse_id", "=", warehouse.id),
                    ("hook_active_stock_variation", "=", True),
                ]
            )
            for channel in channels:
                products_bound = channel.product_product_bindings.mapped("record_id")
                products_to_notify = products_moved & products_bound
                bindings = channel.product_product_bindings.filtered(
                    lambda r: r.record_id in products_to_notify.ids
                )
                qty_variations = bindings._prepare_qty_variations()
                if qty_variations:
                    rec.trigger_channel_hook("stock_variation", products_to_notify)

    def get_hook_content_stock_variation(self, product_qty_mappings):
        return {"name": "stock_variation", "data": product_qty_mappings}

    def _action_cancel(self):
        result = super()._action_cancel()
        self._notify_stock_variation()
        return result

    def _action_confirm(self, merge=True, merge_into=False):
        result = super()._action_confirm(merge, merge_into)
        result._notify_stock_variation()
        return result

    def _action_done(self, cancel_backorder=False):
        result = super()._action_done(cancel_backorder)
        self._notify_stock_variation()
        return result
