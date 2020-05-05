# Copyright 2020 Akretion
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_binding_id = fields.Many2one(
        "res.partner.binding", string="Partner binding", ondelete="set null"
    )
