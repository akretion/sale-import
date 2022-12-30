# Copyright 2021 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    channel_bind_ids = fields.One2many(
        "channel.product.template",
        "record_id",
        string="Channel Binding",
        context={"active_test": False},
    )

    def _create_variant_ids(self):
        res = super()._create_variant_ids()
        self.channel_bind_ids._create_missing_channel_product_product()
        return res
