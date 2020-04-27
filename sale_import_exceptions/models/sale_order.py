# Copyright 2020 Akretion
from odoo import models
from odoo.tools import float_compare


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_amounts_consistency(self):  # TODO clarify logic
        # compare untaxed amounts
        # amount_untaxed_actual = self.amount_untaxed
        amount_untaxed_expected = self.get_amount_untaxed_expected()
        # compare tax amounts
        # amount_tax_actual = self.amount_tax
        amount_tax_expected = self.get_amount_tax_expected()
        # compare total amounts
        amount_total_actual = self.amount_total
        amount_total_expected = amount_untaxed_expected + amount_tax_expected
        if (
            float_compare(
                amount_total_actual, amount_total_expected, precision_digits=2
            )
            == 0
        ):
            return True
        else:
            return False

    def get_amount_untaxed_expected(self):
        total = 0.0
        for line in self.order_line:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            total += line.product_uom_qty * price
        return total

    def get_amount_tax_expected(self):
        """ Mirrors sale.order.line._compute_amount function calculation """
        total_tax = 0.0
        for line in self.order_line:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(
                price,
                line.order_id.currency_id,
                line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id,
            )
            total_tax += taxes
        return total_tax
