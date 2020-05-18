# Copyright 2019 Creu Blanca
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
#     (http://www.eficent.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Job Queue Chunk',
    'version': '12.0.1.0.1',
    'author': 'Akretion',
    'website': 'https://github.com/OCA/queue',
    'license': 'AGPL-3',
    'category': 'Generic Modules',
    'depends': [
        'queue_job',
        'component'
    ],
    'data': [
        'views/queue_job.xml',
        'views/queue_job_chunk.xml',
    ],
}
