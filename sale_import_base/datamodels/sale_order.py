# Copyright 2020 Akretion

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.datamodels.base import BaseDatamodel

FIELDS_REQUIRED_address_customer = ["email"]


class SaleOrderDatamodel(BaseDatamodel):
    _name = "sale.order"

    # @validates("address_customer")
    # def _validate_address_customer(
    #     self, address_customer
    # ):  # TODO: use external_id FIRST + add option match partner on email on
    #  sale_channel,
    #     # en tous les cas, il y a un external id required
    #     email = address_customer.email
    #     if (
    #         len(self.env["res.partner"].search([("email", "=", email)]).ids)
    #         != 1
    #     ):
    #         raise ValidationError("Could not find one contact for given email")

    address_customer = fields.NestedModel("sale.order.address", required=True)
    address_shipping = fields.NestedModel("sale.order.address", required=True)
    address_invoicing = fields.NestedModel("sale.order.address", required=True)
    lines = fields.NestedModel("sale.order.line", many=True, required=True)
    amount = fields.NestedModel("sale.order.amount", required=True)
    payment_mode = fields.Str()
    transaction_id = fields.Integer()
    status = fields.Str()
    invoice = fields.NestedModel("sale.order.invoice.history")

    # can't use this because we need to pass parameters like partner identification
    # via external_id or email which becomes complicated with the
    # datamodel/marshmallowobject/schema hierarchy and schema having only access
    # to raw, static data
    # @pre_dump(pass_many=False)
    # def format_vals(self, sale_order, **kwargs):
    #     """ Returns an odoo-formatted vals dict with the right m2os for addresses
    #      also updates the partner address with supplied address_customer """
    #
    #     # addresses
    #     partner_id = self.env["res.partner"].search(
    #         [("email", "=", sale_order.address_customer.email)]
    #     )
    #     self.env["sale.order"]._update_customer_address_from_import(
    #         partner_id, sale_order.address_customer
    #     )
    #     sale_order.partner_id = partner_id.id
    #     for addr in ("address_shipping", "address_invoicing"):
    #         getattr(sale_order, addr).parent_id = partner_id
    #         self.env["res.partner"].find_or_create_version(
    #             getattr(sale_order, addr)
    #         )
    #     for field_discard in (
    #         "address_customer",
    #         "address_shipping",
    #         "address_invoicing",
    #     ):
    #         delattr(sale_order, field_discard)
    #
    #     # order lines
    #     sale_order.order_line = [(6, 0, vals) for vals in sale_order.lines]
    #     delattr(sale_order, "lines")
    #
    #     # invoice history
    #     sale_order["sale.order.invoice.history"] = (
    #         6,
    #         0,
    #         sale_order["invoice"],
    #     )
    #     delattr(sale_order, "invoice")
    #
    #     return sale_order
