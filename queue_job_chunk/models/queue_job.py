
from odoo import models, fields
from odoo.addons.queue_job.job import job


class QueueJob(models.Model):
    _inherit = "queue.job"

    origin_chunk_id = fields.Many2one("queue.job.chunk")