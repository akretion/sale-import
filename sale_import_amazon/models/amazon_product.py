# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AmazonProduct(models.Model):
    _name = "amazon.product"
    _description = "Amazon Product"  # TODO

    name = fields.Char()
    product_id = fields.Many2one("product.product", string="Odoo Product")
