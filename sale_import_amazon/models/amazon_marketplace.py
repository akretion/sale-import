# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AmazonMarketplace(models.Model):
    _name = "amazon.marketplace"
    _description = "Amazon MarketPlace"
    # List on https://developer-docs.amazon.com/sp-api/docs/marketplace-ids

    # TODO: create xml data with all the Amazon Marketplaces
    name = fields.Char()
    country_code = fields.Char(required=True)
    marketplace_ref = fields.Char()
