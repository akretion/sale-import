# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleChannelPartnerBinding(models.Model):
    _name = "res.partner.binding"
    _description = "Sale Channel Partner Binding"

    sale_order_ids = fields.One2many(
        "sale.order", "partner_binding_id", string="Sale orders"
    )
    sale_channel_id = fields.Many2one(
        "sale.channel", "Sale Channel", required=True, ondelete="cascade"
    )
    partner_id = fields.Many2one(
        "res.partner", "Contact", required=True, ondelete="cascade"
    )
    external_id = fields.Char(
        "External ID", help="The user ID from the external sale channel", required=True
    )
