from odoo.addons.datamodel import fields
from odoo.addons.datamodel.datamodels.base import BaseDatamodel


class SaleOrderPaymentDatamodel(BaseDatamodel):
    _name = "sale.order.payment"

    mode = fields.Str(required=True)
    amount = fields.Decimal()
    reference = fields.Str()
    currency_code = fields.Str()
