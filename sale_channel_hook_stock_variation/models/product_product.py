# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "sale.channel.hook.mixin"]

    def _notify_stock_variation(self, warehouse):
        self.ensure_one()
        binding = self.env["channel.product.product"].search(
            [("product_variant_id", "=", self.id), ("warehouse_id", "=", warehouse.id)]
        )
        variation = binding._prepare_qty_variation()
        if variation:
            self.trigger_channel_hook("stock_variation", variation)

    def get_hook_content_stock_variation(self, variation):
        return {"name": "stock_variation", "data": variation}
