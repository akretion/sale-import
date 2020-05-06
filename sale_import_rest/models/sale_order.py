# Copyright 2020 Akretion

from odoo import _, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _si_get_partner(self, so_vals):
        sale_channel_id = self.env.context.get("sale_channel")
        external_id = so_vals["address_customer"].get("external_id")
        binding = self.env["res.partner.binding"].search(
            [
                ("partner_id", "=", external_id.id),
                ("sale_channel_id", "=", sale_channel_id.id),
            ]
        )
        if binding:
            return binding.partner_id
        if sale_channel_id.allow_match_on_email:
            return super()._si_get_partner(so_vals)
        else:
            raise ValidationError(_("No customer found"))
