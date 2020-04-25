# Copyright 2020 Akretion
from marshmallow_objects import ValidationError, validates

from odoo import _

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.datamodels.base import BaseDatamodel


class SaleOrderAddressDatamodel(BaseDatamodel):
    _name = "sale.order.address"

    @validates("state_code")
    def _validate_state_code(self, code):
        if not code:
            return
        state = self.env["res.country.state"].search([("code", "=", code)])
        if len(state.ids) != 1:
            raise ValidationError(_("Could not determine one state from state code"))

    @validates("country_code")
    def _validate_country_code(self, code):
        country = self.env["res.country"].search([("code", "=", code)])
        if len(country.ids) != 1:
            raise ValidationError(
                _("Could not determine one country from country code")
            )

    name = fields.Str()
    street = fields.Str(required=True)
    street2 = fields.Str()
    zip = fields.Integer(required=True)
    city = fields.Str(required=True)
    email = fields.Email()  # validates in sale_order
    state_code = fields.Str()
    country_code = fields.Str(required=True)
    external_id = fields.Str()

    # @pre_dump
    # def format_vals(self, data, **kwargs):
    #     """ Returns an odoo-formatted vals dict with the right m2os for addresses"""
    #     country_id = self.env["res.country"].search(
    #         [("code", "=", data.country_code)]
    #     )
    #     state_id = self.env["res.country.state"].search(
    #         [("code", "=", data.state_code)]
    #     )
    #     data.country_id = country_id.id
    #     data.state_id = state_id.id
    #     data.pop("country_id")
    #     data.pop("state_id")
    #     return data
