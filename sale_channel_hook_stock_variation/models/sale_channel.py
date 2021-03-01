# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    product_stock_field_id = fields.Many2one(
        "ir.model.fields",
        "Product stock field",
        domain=[
            ("ttype", "in", ["float", "integer"]),
            ("model", "in", ["product.product", "product.template"]),
        ],
        help="Field used to have the current stock of a product.product",
        default=lambda self: self._default_stock_field_id(),
    )

    def _default_stock_field_id(self):
        return self.env.ref("stock.field_product_product__qty_available")

    hook_active_stock_variation = fields.Boolean("Active stock variation hook")
    warehouse_id = fields.Many2one("stock.warehouse")
