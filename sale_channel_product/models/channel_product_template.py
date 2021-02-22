# Copyright 2021 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplateChannel(models.Model):
    _name = "channel.product.template"
    _description = "Product Template Channel"
    _inherits = {"product.template": "record_id"}

    record_id = fields.Many2one(
        "product.template", required=True, ondelete="cascade", index=True
    )
    channel_variant_ids = fields.One2many(
        "channel.product.product", "channel_product_template_id", "Channel Variant"
    )
    active = fields.Boolean(default=True, inverse="_inverse_active")
    channel_id = fields.Many2one("sale.channel", required=True)

    def _inverse_active(self):
        # TODO FIXME
        self.filtered(lambda p: not p.active).mapped("channel_variant_ids").write(
            {"active": False}
        )
        self.filtered(lambda p: p.active).mapped("channel_variant_ids").write(
            {"active": True}
        )

    def _prepare_channel_product_product(self, variant):
        values = {"record_id": variant.id, "channel_product_template_id": self.id}
        # If the variant is not active, we have to force active = False
        if not variant.active:
            values.update({"active": variant.active})
        return values

    def _create_missing_channel_product_product(self):
        """
        Create missing shopinvader.variant and return new just created
        :return: shopinvader.variant recordset
        """
        channel_products = self.env["channel.product.product"]
        for record in self.with_context(active_test=False):
            for variant in record.product_variant_ids:
                if variant not in record.channel_variant_ids.record_id:
                    vals = record._prepare_channel_product_product(variant)
                    channel_products |= self.env["channel.product.product"].create(vals)
        return channel_products

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._create_missing_channel_product_product()
        return record

    def unlink(self):
        # Call unlink manually to be sure to trigger
        # channel.product.product unlink constraint
        self.mapped("channel_variant_ids").unlink()
        return super().unlink()
