#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


from odoo.addons.sale_import_base.models.schemas import Customer, SaleOrder


class ExtendedSaleOrder(SaleOrder, extends=SaleOrder):
    address_shipping: Customer
    address_invoicing: Customer
