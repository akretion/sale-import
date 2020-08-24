# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import hashlib
import hmac

import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    auth_token = fields.Char("Secret authentication token")  # DISCUSSION: sécurité
    api_endpoint = fields.Char("Hooks API endpoint")

    def execute_hook(self, hook_name, content):
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
        payload = {"event": hook_name, "data": content}
        signature = self._generate_hook_signature(payload)
        headers = {"X-Hub-Signature": signature}
        url = self.api_endpoint
        response = requests.post(
            url, data=payload, headers=headers
        )  # DISCUSSION: timeout?
        # DISCUSSION: on fait quoi avec la response ?
        return response

    def _generate_hook_signature(self, content):
        secret = self.auth_token
        signature = hmac.new(
            secret.encode("utf-8"), content.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return signature
