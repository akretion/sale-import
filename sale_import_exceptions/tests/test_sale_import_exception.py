# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.sale_import_base.tests.common_sale_order_import import SaleImportCase


class TestSaleImportException(SaleImportCase):
    """Tests datamodel-level validation"""

    def setUp(self):
        super().setUp()
