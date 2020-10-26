#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import hashlib
import hmac
import json

from odoo.addons.sale.tests.test_sale_common import TestCommonSaleNoChart


class TestSaleChannel(TestCommonSaleNoChart):
    def setUp(self):
        super().setUp()
        self.sale_channel = self.env.ref("sale_channel.sale_channel_amazon")
        self.url = "https://www.example.com/whatever"
        self.payload = json.dumps({"greeting": "Hello!"})
        self.headers = {}

    def test_auth_url_token(self):
        self.sale_channel.auth_method = "url_token"
        headers, payload, url = self.sale_channel._auth_method_url_token(
            self.headers, self.payload, self.url
        )
        self.assertEqual(headers, {})
        self.assertEqual(payload, '{"greeting": "Hello!"}')
        self.assertEqual(
            url, "https://www.example.com/whatever?token=mySecureTokenForHook"
        )

    def test_auth_signature(self):
        self.sale_channel.auth_method = "signature"
        headers, payload, url = self.sale_channel._auth_method_signature(
            self.headers, self.payload, self.url
        )
        signature = hmac.new(
            b"mySecureTokenForHook", payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        self.assertEqual(headers, {"X-Hub-Signature": signature})
        self.assertEqual(payload, '{"greeting": "Hello!"}')
        self.assertEqual(url, "https://www.example.com/whatever")
