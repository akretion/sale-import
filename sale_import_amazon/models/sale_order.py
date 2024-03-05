# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_fulfilled_by_amazon = fields.Boolean()

    def _deliver_order_by_amazon(self):
        # TODO
        pass
