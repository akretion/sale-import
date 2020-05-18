from odoo.addons.component.core import Component


class SaleChannelImporter(Component):
    _name = 'sale.channel.importer'
    _inherit = 'base'

    _usage = 'importer'
    _collection = 'sale.channel'
    _apply_on = ['sale.order']

    def run(self):
        a = 'a'
        return a