#  Copyright (c) Akretion 2021
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    is_white_label = fields.Boolean(
        help="Check this box if this channel comes from a white label partner"
    )
