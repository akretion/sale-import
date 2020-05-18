from odoo.addons.component.core import Component


class QueueJobSplitter(Component):
    _name = 'queue.job.splitter'
    _inherit = 'base'

    _usage = 'job.splitter'
    _collection = 'queue.job.chunk'
    _apply_on = ['queue.job.chunk']

    def run(self, data, target_fn, collection, usage, apply_on):
        splitting_fn = '_split_' + getattr(self, target_fn)
        data_chunks = splitting_fn(data)
        attachment_vals = {
            ''
        }
        attachment = self.env['ir.attachment'].create(attachment_vals)
        result = list()
        for data_chunk in data_chunks:
            job_chunk_vals = {
                'collection': collection,
                'usage': usage,
                'apply_on': apply_on,
                'data_original': attachment,
                'data_str': data_chunk,
            }