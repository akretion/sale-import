# Copyright 2020 Akretion

from odoo import _, models
from odoo.exceptions import ValidationError

from odoo.addons.queue_job.job import job


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @job
    def process_json_import(self, data, **kwargs):
        if not kwargs.get("sale_channel"):
            raise ValidationError(
                _("You need to specify a sale channel to import a sales order")
            )
        self = self.with_context({"sale_channel": kwargs.get("sale_channel")})
        super().process_json_import(data)

    def _si_finalize(self, data):
        sale_channel = self.env.context.get("sale_channel")
        self.sale_channel_id = sale_channel
        self._si_create_sale_channel_binding(data)

    def _si_create_sale_channel_binding(self, data):
        binding_vals = {
            "channel_id": self.sale_channel_id.id,
            "partner_id": self.partner_id.id,
            "external_id": data["customer_address"]["external_id"],
        }
        self.env["sale.channel.partner.binding"].create(binding_vals)

    def _si_get_partner(self, so_vals):
        sale_channel_id = self.env.context.get("sale_channel")
        external_id = so_vals["address_customer"].get("external_id")
        binding = self.env["sale.channel.partner.binding"].search(
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
