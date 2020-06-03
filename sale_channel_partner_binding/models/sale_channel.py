#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from odoo import _, fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    def _compute_count_bindings(self):
        for rec in self:
            rec.count_bindings = len(rec.partner_bind_ids.ids)

    partner_bind_ids = fields.One2many(
        "res.partner.binding", "sale_channel_id", string="Channel bindings"
    )
    count_bindings = fields.Integer(string="Bindings", compute=_compute_count_bindings)

    def button_open_bindings(self):
        tree_view_id = self.env.ref(
            "sale_channel_partner_binding.partner_binding_view_tree"
        ).id
        act = {
            "name": _("Partner bindings"),
            "res_model": "res.partner.binding",
            "type": "ir.actions.act_window",
            "views": [(tree_view_id, "tree")],
            "domain": [("id", "in", self.partner_bind_ids.ids)],
        }
        return act
