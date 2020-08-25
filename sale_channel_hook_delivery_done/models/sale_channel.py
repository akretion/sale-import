#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    hook_active_delivery_done = fields.Boolean("Active delivery done hook")
