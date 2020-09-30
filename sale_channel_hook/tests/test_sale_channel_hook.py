#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.addons.sale.tests.test_sale_common import TestCommonSaleNoChart
import hashlib
import hmac
import json


class TestSaleChannel(TestCommonSaleNoChart):
    def setUp(self):
        super().setUp()
        self.sale_channel = self.env.ref("sale_channel.sale_channel_amazon")
        self.url = "https://www.example.com/webhooks/whatever"
        self.payload = {"greeting": "Hello!"}
        self.headers = {}

    def test_auth_basic(self):
        self.sale_channel.auth_method = "basic"
        headers, payload, url = self.sale_channel._auth_method_basic(self.headers, self.payload, self.url)
        self.assertEqual(headers, {})
        self.assertEqual(payload, {"greeting": "Hello!"})
        self.assertEqual(url, "https://www.example.com/webhooks/whatever?token=mySecureTokenForHook")

    def test_auth_signature(self):
        self.sale_channel.auth_method = "signature"
        headers, payload, url = self.sale_channel._auth_method_signature(self.headers, self.payload, self.url)
        payload_str = json.dumps(payload)
        signature = hmac.new(
            "mySecureTokenForHook".encode("utf-8"), payload_str.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        self.assertEqual(headers, {"X-Hub-Signature": signature})
        self.assertEqual(payload, {"greeting": "Hello!"})
        self.assertEqual(url, "https://www.example.com/webhooks/whatever")
