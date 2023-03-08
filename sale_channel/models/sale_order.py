#  Copyright (c) Akretion 2020
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_channel_id = fields.Many2one("sale.channel", ondelete="restrict")

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        res["sale_channel_id"] = self.sale_channel_id.id
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("sale_channel_id"):
                channel = self.env["sale.channel"].browse(vals["sale_channel_id"])
                if channel.sequence_id:
                    seq_date = None
                    if "date_order" in vals:
                        seq_date = fields.Datetime.context_timestamp(
                            self, fields.Datetime.to_datetime(vals["date_order"])
                        )
                    vals["name"] = channel.sequence_id._next(seq_date)
        return super().create(vals_list)
