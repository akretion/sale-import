# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplateChannel(models.Model):
    _inherit = "channel.product.template"

    sale_channel_id = fields.Many2one("sale.channel")
