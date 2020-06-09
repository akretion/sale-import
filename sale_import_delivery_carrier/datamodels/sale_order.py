from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class SaleOrderDatamodel(Datamodel):
    _inherit = "sale.order"

    delivery_carrier = fields.NestedModel("delivery.carrier")
