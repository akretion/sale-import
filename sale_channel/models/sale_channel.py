# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleChannel(models.Model):
    _name = "sale.channel"
    _description = "Sale Channel"

    name = fields.Char("Name", required=True)
