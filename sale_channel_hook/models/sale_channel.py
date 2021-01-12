#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import hashlib
import hmac
import json

import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SaleChannel(models.Model):
    _name = "sale.channel"
    _inherit = ["sale.channel", "server.env.mixin"]

    auth_token = fields.Char("Secret authentication token")
    api_endpoint = fields.Char("Hooks API endpoint")
    auth_method = fields.Selection(
        [("none", "None"), ("url_token", "URL Token"), ("signature", "Signature")]
    )

    def _auth_method_none(self, headers, payload, url):
        return headers, payload, url

    def _auth_method_url_token(self, headers, payload, url):
        """
        Add token to URL as a parameter:
        Simply adds a ?<token> at the end of the url
        """
        url += "?token=" + self.auth_token
        return headers, payload, url

    def _generate_hook_request_signature(self, payload):
        """
        Use the token to sign the request:
        - encode the secret token in utf-8
        - use the encoded token as key when you
        - hash the request's utf-8-encoded payload in sha256.
        """
        secret = self.auth_token
        signature = hmac.new(
            secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return signature

    def _auth_method_signature(self, headers, payload, url):
        """
        In principle, the sending side will calculate a hash using the secret token
        and the request's contents, that hash will be used as a signature.
        Then, the receiving side will do exactly the same calculation using the same
         secret. If the signatures are the same, treat the request as valid.
        """
        headers["X-Hub-Signature"] = self._generate_hook_request_signature(payload)
        return headers, payload, url

    def _apply_webhook_security(self, headers, payload, url):
        auth_fn_name = "_auth_method_{}".format(self.auth_method or 'none')
        auth_fn = getattr(self, auth_fn_name)
        return auth_fn(headers, payload, url)

    @property
    def _server_env_fields(self):
        result = super()._server_env_fields
        sale_channel_fields = {"auth_token": {},
                            "auth_method": {},
                            "api_endpoint": {}}
        result.update(sale_channel_fields)
        return result

    def send_hook_api_request(self, content):
        if not self.api_endpoint or not self.auth_token:
            raise ValidationError(
                _(
                    "Set a secret token and define an API "
                    "endpoint to use this channel's hook"
                )
            )
        url = self.api_endpoint
        payload = json.dumps(content)
        headers, payload, url = self._apply_webhook_security({}, payload, url)
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response
