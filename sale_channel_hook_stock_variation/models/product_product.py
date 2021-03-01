# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _notify_stock_variation(self):
        self.ensure_one()
        bindings = self.env["channel.product.product"].search(
            [("product_variant_id", "=", self.id)]
        )
        for binding in bindings:
            binding._notify_stock_variation()
