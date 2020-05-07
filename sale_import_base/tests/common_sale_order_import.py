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
        cls.setUpTaxes()
        cls.setUpFpos()

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
        cls.addr_customer_example = {
            "name": "Thomas Jean",
            "street": "1 rue de Jean",
            "street2": "bis",
            "zip": "69100",
            # 'state_code': 'CR-SJ',
            "city": "Lyon",
            "email": "thomasjean@gmail.com",
            "country_code": "FR",
            "external_id": "EBAY_CUST123",
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
        amt_untaxed_1 = (
            cls.line_valid_1["price_unit"]
            * cls.line_valid_1["qty"]
            * (1 - cls.line_valid_1["discount"] / 100)
        )
        amt_tax_1 = amt_untaxed_1 * 0.09
        amt_total_1 = amt_untaxed_1 + amt_tax_1
        amt_untaxed_2 = cls.line_valid_2["price_unit"] * cls.line_valid_2["qty"]
        amt_tax_2 = amt_untaxed_1 * 0.09
        amt_total_2 = amt_untaxed_1 + amt_tax_1
        cls.amount_valid = {
            "amount_tax": amt_tax_1 + amt_tax_2,
            "amount_untaxed": amt_untaxed_1 + amt_untaxed_2,
            "amount_total": amt_total_1 + amt_total_2,
        }
        cls.amount_invalid = {
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
            "currency_code": "EUR",
        }
        binding_vals = {
            "sale_channel_id": cls.sale_channel_ebay.id,
            "partner_id": cls.partner_thomasjean.id,
            "external_id": "EBAY_CUST123",
        }
        cls.env["res.partner.binding"].create(binding_vals)

    @classmethod
    def setUpTaxes(cls):
        Tax = cls.env["account.tax"]
        tax_vals = {
            "name": "tax 9%",
            "amount": "9.00",
            "type_tax_use": "sale",
            "company_id": cls.env.ref("base.main_company").id,
        }
        cls.tax = Tax.create(tax_vals)
        cls.product_order.taxes_id = cls.tax

    @classmethod
    def setUpFpos(cls):
        """ CH: taxes, DE: no taxes """
        Tax = cls.env["account.tax"]
        Fpos = cls.env["account.fiscal.position"]
        FposLine = cls.env["account.fiscal.position.tax"]

        # CH
        fpos_vals_swiss = {
            "name": "Swiss Fiscal Position",
            "country_id": cls.env.ref("base.ch").id,
            "zip_from": 0,
            "zip_to": 0,
            "auto_apply": True,
        }
        cls.fpos_swiss = Fpos.create(fpos_vals_swiss)
        tax_vals_swiss = {
            "name": "Tax Swiss",
            "amount": "15.00",
            "type_tax_use": "sale",
            "company_id": cls.env.ref("base.main_company").id,
        }
        cls.tax_swiss = Tax.create(tax_vals_swiss)
        fpos_line_vals = {
            "position_id": cls.fpos_swiss.id,
            "tax_src_id": cls.tax.id,
            "tax_dest_id": cls.tax_swiss.id,
        }
        FposLine.create(fpos_line_vals)

        # DE
        fpos_vals_de = {
            "name": "German Fiscal Position",
            "country_id": cls.env.ref("base.de").id,
            "zip_from": 0,
            "zip_to": 0,
            "auto_apply": True,
        }
        cls.fpos_de = Fpos.create(fpos_vals_de)
        fpos_line_vals = {"position_id": cls.fpos_de.id, "tax_src_id": cls.tax.id}
        FposLine.create(fpos_line_vals)
