# Copyright 2020 Akretion

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.datamodels.base import BaseDatamodel


class DeliveryCarrierDatamodel(BaseDatamodel):
    _name = "delivery.carrier"

    name = fields.Str(required=True)
    price_unit = fields.Decimal(required=True)
    discount = fields.Decimal(required=True)
    description = fields.Str()
