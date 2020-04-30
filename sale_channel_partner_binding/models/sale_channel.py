# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    sale_channel_partner_bind_ids = fields.One2many(
        "sale.channel.partner.binding", "sale_channel_id", string="Channel bindings"
    )
