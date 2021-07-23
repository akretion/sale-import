#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class DeliveryCarrierDatamodel(Datamodel):
    _name = "delivery.carrier"

    name = fields.Str(required=True)
    price_unit = fields.Decimal(required=True)
    discount = fields.Decimal()
    description = fields.Str()
