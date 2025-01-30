import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-akretion-sale-import",
    description="Meta package for akretion-sale-import Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-queue_job_chunk',
        'odoo14-addon-sale_channel',
        'odoo14-addon-sale_channel_hook',
        'odoo14-addon-sale_channel_hook_delivery_done',
        'odoo14-addon-sale_channel_hook_invoice',
        'odoo14-addon-sale_channel_hook_sale_state',
        'odoo14-addon-sale_channel_hook_stock_variation',
        'odoo14-addon-sale_channel_partner',
        'odoo14-addon-sale_channel_product',
        'odoo14-addon-sale_channel_white_label',
        'odoo14-addon-sale_import_base',
        'odoo14-addon-sale_import_delivery_carrier',
        'odoo14-addon-sale_import_rest',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
