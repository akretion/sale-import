# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleChannelPartnerBinding(models.Model):
    _name = "sale.channel.partner.binding"
    _description = "Sale Channel Partner Binding"

    sale_channel_id = fields.Many2one("sale.channel", "Sale Channel")
    partner_id = fields.Many2one("res.partner", "Contact")
    external_id = fields.Char(
        "External ID", help="The user ID from the external sale channel"
    )
