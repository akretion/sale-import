# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    amazon_product_ids = fields.One2many("amazon.product", "product_id")
