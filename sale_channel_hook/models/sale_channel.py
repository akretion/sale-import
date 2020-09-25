#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.queue_job.job import job


class SaleChannel(models.Model):
    _name = "sale.channel"
    _inherit = ["sale.channel", "server.env.mixin"]

    auth_token = fields.Char("Secret authentication token")
    api_endpoint = fields.Char("Hooks API endpoint")

    def _apply_webhook_security(self, headers, payload, url):
        """ Extend this function to customize hook security """
        return headers, payload, url

    @property
    def _server_env_fields(self):
        result = super()._server_env_fields
        sale_channel_fields = {"auth_token": {}}
        result.update(sale_channel_fields)
        return result

    @job
    def send_hook_api_request(self, hook_name, content):
        # check necessary info is filled
        if not self.api_endpoint or not self.auth_token:
            raise ValidationError(
                _(
                    "Set a secret token and define an API "
                    "endpoint to use this channel's hook"
                )
            )
        # check hook is activated
        if not getattr(self, "hook_active_" + hook_name):
            return
        url = self.api_endpoint + hook_name
        headers, payload, url = self._apply_webhook_security({}, content, url)
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response
