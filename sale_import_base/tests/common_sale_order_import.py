# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.datamodel.tests.common import SavepointDatamodelCase
from odoo.addons.sale.tests.test_sale_common import TestCommonSaleNoChart


class SaleImportCase(SavepointDatamodelCase, TestCommonSaleNoChart):
    @classmethod
    def setUpClass(cls):
        super(SaleImportCase, cls).setUpClass()
        cls._setup_data()

    @classmethod
    def _setup_data(cls):
        cls.partner_thomasjean = cls.env["res.partner"].create(
            {
                "name": "Thomas Jean",
                "email": "thomasjean@gmail.com",
                "street": "initial address",
                "street2": "initial address2",
                "zip": "0",
                "city": "initial city",
                "country_id": cls.env.ref("base.fr").id,
            }
        )
        cls.addr_customer_minimum = {
            "name": "Thomas Jean",
            "street": "1 rue de xyz",
            # street2: not required
            "zip": "69100",
            "city": "Lyon",
            "email": "thomasjean@gmail.com",
            # state_code: not required
            # "state_code": 69001,
            "country_code": "FR",
        }
        cls.addr_shipping_minimum = {
            "name": "does not matter",
            "street": "2 rue de xyz",
            "zip": "69100",
            # street2: not required
            "city": "Lyon",
            # email: not required
            # state_code: not required
            "country_code": "FR",
        }
        cls.addr_invoicing_minimum = {
            "name": "does not matter",
            "street": "3 rue de xyz",
            "zip": "69100",
            # street2: not required
            "city": "Lyon",
            # email: not required
            # state_code: not required
            "country_code": "FR",
        }
        cls.addr_customer_example = {
            "name": "Thomas Jean",
            "street": "1 rue de Jean",
            "street2": "bis",
            "zip": "69100",
            # 'state_code': 'CR-SJ',
            "city": "Lyon",
            "email": "thomasjean@gmail.com",
            "country_code": "FR",
        }
        cls.addr_shipping_example = {
            "name": "shipping contact name",
            "street": "2 rue de shipping",
            "street2": "bis",
            "zip": "69100",
            # 'state_code': 'CR-SJ',
            "city": "Lyon",
            "email": "not-required@not-required.com",
            "country_code": "FR",
        }
        cls.addr_invoicing_example = {
            "name": "invoicing contact name",
            "street": "3 rue de invoicing",
            "street2": "bis",
            "zip": "69100",
            "city": "Lyon",
            "email": "whatever@whatever.io",
            # 'state_code': 'CR-SJ',
            "country_code": "FR",
        }
        cls.addr_customer_missing_field = {
            "name": "Thomas Jean",
            "street": "1 rue de xyz",
            # street2: not required
            "city": "Lyon",
            "email": "thomasjean@gmail.com",
            # state_code: not required
            # country_code: required, missing
            # external_id: not required
        }
        cls.addr_shipping_missing_field = {
            "name": "does not matter",
            # street: required, missing
            # street2: not required
            "city": "Lyon",
            # email: not required
            # state_code: not required
            "country_code": "FR",
            # external_id: not required
        }
        cls.addr_invoicing_missing_field = {
            # name: required, missing
            "street": "3 rue de xyz",
            # street2: not required
            "city": "Lyon",
            # email: not required
            # state_code: not required
            "country_code": "FR",
            # external_id: not required
        }
        cls.line_valid_1 = {
            "product_code": "FURN_0096",
            "qty": 5,
            "price_unit": 500.0,
            "description": "Some description",
            "discount": 0.0,
        }
        cls.line_valid_2 = {
            "product_code": "E-COM10",
            "qty": 2,
            "price_unit": 200.0,
            "description": "",
            "discount": 0.0,
        }
        cls.line_invalid = {
            "product_code": "DOES NOT EXIST",
            "qty": 5,
            "price_unit": 500.0,
            "description": "",
            "discount": 0.0,
        }
        cls.amount_valid = {
            # note: this is for syntax check only
            "amount_tax": 2500.0 * 5 * 0.15,
            "amount_untaxed": 2500.0 * 5,
            "amount_total": 2500.0 * 5 * 1.15,
        }
        cls.amount_invalid = {
            # note: this is for syntax check only
            "amount_tax": "this should not",
            "amount_untaxed": "happen",
            "amount_total": dict(),
        }
        cls.invoice_history_example = {"date": "1900-12-30", "number": "IN-123"}
        cls.sale_order_example = {
            "address_customer": cls.addr_customer_example,
            "address_shipping": cls.addr_shipping_example,
            "address_invoicing": cls.addr_invoicing_example,
            "lines": [cls.line_valid_1, cls.line_valid_2],
            "amount": cls.amount_valid,
            "payment_mode": "Does not matter",
            "transaction_id": 123,
            "status": "Does not matter",
            "invoice": cls.invoice_history_example,
        }
        cls.sale_channel_ebay = cls.ref("sale_channel.sale_channel_ebay")
