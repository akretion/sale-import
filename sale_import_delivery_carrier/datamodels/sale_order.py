# Copyright 2020 Akretion

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.datamodels.base import BaseDatamodel


class SaleOrderDatamodel(BaseDatamodel):
    _inherit = "sale.order"

    delivery_carrier = fields.NestedModel("delivery.carrier")
