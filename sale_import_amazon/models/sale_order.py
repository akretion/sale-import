# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_fulfilled_by_amazon = fields.Boolean()
    amazon_marketplace_id = fields.Many2one("amazon.marketplace")

    def _deliver_order_by_amazon(self):
        self.ensure_one()
        self.sale_channel_id.amazon_location_id
        # TODO
