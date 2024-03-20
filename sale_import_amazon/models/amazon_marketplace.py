# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AmazonMarketplace(models.Model):
    _name = "amazon.marketplace"
    _description = "Amazon MarketPlace"

    name = fields.Char()
    country_code = fields.Char(required=True)
    marketplace_ref = fields.Char(help="API Marketplace's identifier")
