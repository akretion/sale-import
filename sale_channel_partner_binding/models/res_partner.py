# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_bind_ids = fields.One2many(
        "res.partner.binding", "partner_id", string="Channel bindings"
    )
