# Copyright 2021 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProductChannel(models.Model):
    _name = "channel.product.product"
    _description = "Product Product Channel"
    _inherits = {
        "channel.product.template": "channel_product_template_id",
        "product.product": "record_id",
    }

    channel_product_template_id = fields.Many2one(
        "channel.product.template", required=True, ondelete="cascade", index=True
    )
    record_id = fields.Many2one(
        "product.product", required=True, ondelete="cascade", index=True
    )
    active = fields.Boolean(default=True)

    def write(self, vals):
        super().write(vals)
        if "active" in vals:
            # if we active a variant we have to active the template
            self.filtered("active").channel_product_template_id.filtered(
                lambda s: not s.active
            ).write({"active": True})
            # if we inactive a variant and all variant are inactive
            # the template must be inactivated
            for template in self.filtered(
                lambda s: not s.active
            ).channel_product_template_id:
                if template.active and not any(
                    template.mapped("channel_variant_ids.active")
                ):
                    template.active = False
        return True
