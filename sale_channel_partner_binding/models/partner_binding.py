# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleChannelPartnerBinding(models.Model):
    _name = "res.partner.binding"
    _description = "Sale Channel Partner Binding"
    _sql_constraints = [
        (
            "partner_channel_uniq",
            "unique(partner_id, sale_channel_id)",
            "partner-channel pairs for bindings are unique",
        ),
        (
            "external_id_channel_uniq",
            "unique(external_id, sale_channel_id)",
            "external_id-channel pairs for bindings are unique",
        ),
    ]

    sale_channel_id = fields.Many2one(
        "sale.channel", "Sale Channel", required=True, ondelete="cascade"
    )
    partner_id = fields.Many2one(
        "res.partner", "Contact", required=True, ondelete="cascade"
    )
    external_id = fields.Char(
        "External ID", help="The user ID from the external sale channel", required=True
    )
