# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    sale_channel_partner_bind_ids = fields.One2many(
        "sale.channel.partner.binding", "partner_id", string="Channel bindings"
    )
