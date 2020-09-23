#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import hashlib
import hmac

import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.queue_job.job import job


class SaleChannel(models.Model):
    _name = "sale.channel"
    _inherit = ["sale.channel", "server.env.mixin"]

    auth_token = fields.Char("Secret authentication token")
    api_endpoint = fields.Char("Hooks API endpoint")

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
        payload = {content}
        signature = self._generate_hook_request_signature(payload)
        headers = {"X-Hub-Signature": signature}
        url = self.api_endpoint + hook_name
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response

    def _generate_hook_request_signature(self, content):
        secret = self.auth_token
        signature = hmac.new(
            secret.encode("utf-8"), content.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return signature
