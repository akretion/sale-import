# Copyright 2020 Akretion

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.datamodels.base import BaseDatamodel

FIELDS_REQUIRED_address_customer = ["email"]


class SaleOrderDatamodel(BaseDatamodel):
    _name = "sale.order"

    address_customer = fields.NestedModel("sale.order.address", required=True)
    address_shipping = fields.NestedModel("sale.order.address", required=True)
    address_invoicing = fields.NestedModel("sale.order.address", required=True)
    lines = fields.NestedModel("sale.order.line", many=True, required=True)
    amount = fields.NestedModel("sale.order.amount", required=True)
    payment_mode = fields.Str()
    transaction_id = fields.Integer()
    status = fields.Str()
    invoice = fields.NestedModel("sale.order.invoice.history")
    sale_channel = fields.Str()
