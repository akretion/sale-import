# Copyright 2020 Akretion
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_binding_ids = fields.One2many(
        "res.partner.binding", "sale_order_id", string="Partner bindings"
    )
