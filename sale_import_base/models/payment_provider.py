# Copyright 2022 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    # code is renamed in ref in v16
    # we keep it as is, to keep compatibility only in v14
    code = fields.Char(string="code", related="ref")
    ref = fields.Char()

    _sql_constraints = [("uniq_ref", "uniq(ref)", "The Acquirer ref must be uniq")]
