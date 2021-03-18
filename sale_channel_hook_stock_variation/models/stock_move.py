# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _check_stock_variation(self):
        self.product_id.channel_bind_ids._check_stock_variation()

    def _action_cancel(self):
        result = super()._action_cancel()
        self._check_stock_variation()
        return result

    def _action_confirm(self, merge=True, merge_into=False):
        result = super()._action_confirm(merge=merge, merge_into=merge_into)
        self._check_stock_variation()
        return result

    def _action_assign(self):
        result = super()._action_assign()
        self._check_stock_variation()
        return result

    def _action_done(self, cancel_backorder=False):
        result = super()._action_done(cancel_backorder=cancel_backorder)
        self._check_stock_variation()
        return result
