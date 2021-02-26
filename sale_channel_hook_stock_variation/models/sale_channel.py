# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    hook_active_stock_variation = fields.Boolean("Active stock variation hook")
    warehouse_id = fields.Many2one("stock.warehouse")
