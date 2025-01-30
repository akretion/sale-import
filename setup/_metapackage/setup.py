import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-akretion-sale-import",
    description="Meta package for akretion-sale-import Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-queue_job_chunk',
        'odoo12-addon-sale_channel',
        'odoo12-addon-sale_channel_hook',
        'odoo12-addon-sale_channel_hook_delivery_done',
        'odoo12-addon-sale_channel_hook_invoice',
        'odoo12-addon-sale_channel_hook_sale_state',
        'odoo12-addon-sale_channel_partner',
        'odoo12-addon-sale_import_base',
        'odoo12-addon-sale_import_delivery_carrier',
        'odoo12-addon-sale_import_rest',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)
