#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class SaleOrderDatamodel(Datamodel):
    _inherit = "sale.order"

    delivery_carrier = fields.NestedModel("delivery.carrier")
