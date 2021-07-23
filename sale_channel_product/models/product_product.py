# Copyright 2021 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    channel_bind_ids = fields.One2many(
        "channel.product.product",
        "record_id",
        string="Channel Binding",
        context={"active_test": False},
    )
