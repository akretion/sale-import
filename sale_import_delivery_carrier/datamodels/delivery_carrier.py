#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from marshmallow_objects import ValidationError, validates

from odoo import _

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class DeliveryCarrierDatamodel(Datamodel):
    _name = "delivery.carrier"

    @validates("name")
    def _validate_name(self, name):
        carrier = self._env["delivery.carrier"].search([("name", "=", name)])
        if not carrier:
            raise ValidationError(_("Couldn't find a carrier with given name"))

    name = fields.Str(required=True)
    price_unit = fields.Decimal(required=True)
    discount = fields.Decimal()
    description = fields.Str()
