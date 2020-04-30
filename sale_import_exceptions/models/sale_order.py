# Copyright 2020 Akretion
from odoo import models
from odoo.tools import float_compare


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_amounts_consistency(self):  # TODO clarify logic
        result = True
        for amt_name in ("amount_untaxed", "amount_tax", "amount_total"):
            amt = getattr(self, amt_name)
            amt_imported = getattr(self, "si_" + amt_name)
            if float_compare(amt, amt_imported, precision_digits=2) != 0:
                result = False
        return result
