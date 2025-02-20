# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class SaleChannel(models.Model):
    _name = "sale.channel"
    _inherit = ["sale.channel", "server.env.mixin"]

    lwa_appid = fields.Char(string="LWA App ID")
    sp_api_refresh_token = fields.Char(string="SP-API Refresh Token")
    lwa_client_secret = fields.Char(string="LWA Client Secret")
    is_amazon_channel = fields.Boolean(compute="_compute_is_amazon_channel")

    marketplace_ids = fields.Many2many(
        "amazon.marketplace",
        string="MarketPlaces",
        help="List of the MarketPlaces to be sync with Odoo through this backend app",
    )

    @api.depends("channel_type")
    def _compute_is_amazon_channel(self):
        for rec in self:
            rec.is_amazon_channel = rec.channel_type and rec.channel_type.startswith(
                "amazon"
            )

    @property
    def _server_env_fields(self):
        result = super()._server_env_fields
        sale_channel_fields = {
            "lwa_appid": {},
            "sp_api_refresh_token": {},
            "lwa_client_secret": {},
        }
        result.update(sale_channel_fields)
        return result

    def amazon_get_credentials(self):
        return dict(
            lwa_app_id=self.lwa_appid,
            refresh_token=self.sp_api_refresh_token,
            lwa_client_secret=self.lwa_client_secret,
        )
