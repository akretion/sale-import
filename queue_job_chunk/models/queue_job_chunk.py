
from odoo import models, fields
from odoo.addons.queue_job.job import job


class QueueJobChunk(models.Model):
    _name = "queue.job.chunk"

    def _compute_reference(self):
        for rec in self:
            model = rec.model_id
            record = rec.record_id
            if model and record:
                rec.reference = self.env[model].browse(record)

    # component fields
    usage = fields.Char("Usage")
    collection = fields.Char("Collection")
    apply_on_model = fields.Char("Apply on model")

    data_original = fields.Many2one("ir.attachment", string="Original data")
    data_str = fields.Text(string="Editable data")
    state = fields.Selection([
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('failed', 'Failed')
    ], default='pending', string="State")
    model_id = fields.Integer("Model ID")
    record_id = fields.Integer("Record ID")
    reference = fields.Reference(string="Reference", compute=_compute_reference)
    job_ids = fields.Many2many("queue.job", string="Jobs launched")

    def create(self, vals):
        result = super().create(vals)
        result.process_chunk()
        return result

    def button_retry(self):
        self.process_chunk()

    def process_chunk(self):
        job = self.with_delay()._process_chunk()
        self.job_ids += job
        return job

    @job
    def _process_chunk(self):
        self.ensure_one()
        usage = self.usage
        collection = self.collection
        apply_on = self.apply_on_model
        self.model_id = apply_on
        with collection.work_on(apply_on) as work:
            processor = work.component(usage=usage)
            processor.run(self.data_str)