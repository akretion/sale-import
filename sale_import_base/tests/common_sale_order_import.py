# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.datamodel.tests.common import SavepointDatamodelCase
from odoo.addons.sale.tests.test_sale_common import TestCommonSaleNoChart


class SaleImportCase(SavepointDatamodelCase, TestCommonSaleNoChart):
    @classmethod
    def setUpClass(cls):
        super(SaleImportCase, cls).setUpClass()
        cls.setUpClassicProducts()
        cls.setUpAddresses()
        cls.setUpLines()
        cls.setUpImport()
        cls.setUpTaxesFpos()

    @classmethod
    def setUpAddresses(cls):
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
            "external_id": "AMZN_CUST123",
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

    @classmethod
    def setUpLines(cls):
        cls.line_valid_1 = {
            "product_code": "PROD_ORDER",
            "qty": 5,
            "price_unit": 1111.1,
            "description": "Some description",
            "discount": 10.0,
        }
        cls.line_valid_2 = {
            "product_code": "PROD_DEL",
            "qty": 2,
            "price_unit": 2222.2,
            # description: missing
            "discount": 0.0,
        }
        cls.line_invalid = {
            "product_code": "DOES NOT EXIST",
            "qty": "should not happen",
            "price_unit": "wrong input",
            "description": "",
            "discount": 0.0,
        }

    @classmethod
    def setUpImport(cls):
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
        cls.sale_channel_ebay = cls.env.ref("sale_channel.sale_channel_ebay")
        cls.sale_order_example_vals = {
            "address_customer": cls.addr_customer_example,
            "address_shipping": cls.addr_shipping_example,
            "address_invoicing": cls.addr_invoicing_example,
            "lines": [cls.line_valid_1, cls.line_valid_2],
            "amount": cls.amount_valid,
            "payment_mode": "Does not matter",
            "transaction_id": 123,
            "status": "Does not matter",
            "invoice": cls.invoice_history_example,
            "sale_channel": cls.sale_channel_ebay.name,
            "delivery_carrier": "Normal Delivery Charges",
        }

    @classmethod
    def setUpTaxesFpos(cls):
        Tax = cls.env["account.tax"]
        # Fpos = cls.env["account.fiscal.position"]
        # FposLine = cls.env["account.fiscal.position.tax"] # TODO

        tax_vals = {
            "name": "tax 9%",
            "amount": "9.00",
            "type_tax_use": "sale",
            "company_id": cls.env.ref("base.main_company").id,
        }
        cls.tax = Tax.create(tax_vals)
        # fpos_vals = {"name": "fiscal position"} # TODO use that or not ?
        # cls.fpos = cls.Fpos.create(fpos_vals)
        # fpos_line_vals = {
        #     "position_id": cls.fpos.id,
        #     "tax_src_id": cls.tax.id,
        #     "tax_dest_id": cls.tax.id,
        # }
        # cls.fpos_line = cls.FposLine.create(fpos_line_vals)
        # cls.partner_thomasjean.fiscal_position_id = cls.fpos
        cls.product_order.taxes_id = cls.tax