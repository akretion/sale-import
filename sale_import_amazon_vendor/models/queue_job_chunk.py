# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class QueueJobChunk(models.Model):
    _inherit = "queue.job.chunk"

    processor = fields.Selection(
        selection_add=[
            (
                "sale_channel_importer_amazon_vendor",
                "Sale Channel Importer Amazon Vendor",
            )
        ]
    )

    def _get_processor(self):
        if self.processor == "sale_channel_importer_amazon_vendor":
            return self.env["sale.channel.importer.amazon.vendor"].new(
                {"chunk_id": self.id}
            )
        else:
            return super()._get_processor()
