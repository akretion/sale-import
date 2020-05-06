# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.sale_import_base.tests.common_sale_order_import import SaleImportCase


class TestSaleOrderImport(SaleImportCase):
    def setUp(self):
        super().setUp()
        self.sale_order_example_vals = {
            "payment": {
                "mode": "xyz",
                "amount": "xyz",
                "reference": "xyz",
                "currency_code": "xyz",
            }
        }

    def test_payment_processed(self):
        pass
