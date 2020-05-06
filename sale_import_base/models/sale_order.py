from odoo import _, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.queue_job.job import job

MAPPINGS_SALE_ORDER_ADDRESS_SIMPLE = [
    "name",
    "street",
    "street2",
    "zip",
    "city",
    "external_id",
    "email",
]


class SaleOrder(models.Model):
    _inherit = "sale.order"

    si_exc_check_amounts_untaxed = fields.Boolean(
        "(technical) Check untaxed amounts against imported values"
    )
    si_exc_check_amounts_total = fields.Boolean(
        "(technical) Check total amounts against imported values"
    )
    si_amount_untaxed = fields.Float("(technical) Untaxed amount from import")
    si_amount_tax = fields.Float("(technical) Tax amount from import")
    si_amount_total = fields.Float("(technical) Total amount from import")

    def batch_process_json_imports(self, imports, **kwargs):
        """
        For an up-to-date version of the imports format, check:
            1. datamodels
            2. _si_validate_datamodel function
        kwargs effectively function as way to pass context to jobs
        methods prefixed by "si" are related to sale imports
        """
        jobs = self.env["queue.job"]
        for el in imports:
            new_job = self.with_delay(self.process_json_import(el, kwargs))
            jobs += new_job
        return jobs

    @job
    def process_json_import(self, data, **kwargs):
        so_datamodel = self.env.datamodels["sale.order"].load(data)
        # validation and value processing: we could extend datamodel with the same idea
        self._si_validate_datamodel(so_datamodel)
        so_dump_raw = so_datamodel.dump()
        so_vals = self._si_process_dump(so_dump_raw)
        new_sale_order = self.env["sale.order"].create(so_vals)
        new_sale_order._si_finalize(new_sale_order, data)
        return new_sale_order

    # DATAMODEL VALIDATORS
    def _si_validate_datamodel(self, datamodel_instance):
        """ Extend this method to add your validators against the DB """
        self._si_validate_address_customer(datamodel_instance)
        self._si_validate_product_codes(datamodel_instance)
        self._si_validate_sale_channel(datamodel_instance)
        self._si_validate_currency_code(datamodel_instance)
        self._si_validate_payment(datamodel_instance)

    def _si_validate_address_customer(self, datamodel_instance):
        partner = self.env["res.partner"].search(
            [("email", "=", datamodel_instance.address_customer.email)]
        )
        if len(partner.ids) != 1:
            raise ValidationError(_("Could not find one partner"))

    def _si_validate_product_codes(self, datamodel_instance):
        for line in datamodel_instance.lines:
            product = self.env["product.product"].search(
                [("default_code", "=", line.product_code)]
            )
            if len(product.ids) != 1:
                raise ValidationError(_("Could not find one product"))

    def _si_validate_sale_channel(self, datamodel_instance):
        sale_channel = self.env["sale.channel"].search(
            [("name", "=", datamodel_instance.sale_channel)]
        )
        if len(sale_channel.ids) != 1:
            raise ValidationError(_("Could not find one sale channel"))

    def _si_validate_currency_code(self, datamodel_instance):
        pass  # todo

    def _si_validate_payment(self, datamodel_instance):
        pass  # todo

    # DATAMODEL PROCESSORS
    def _si_process_dump(self, so_vals):
        """ Transform values in-place
         to make it usable in create() """
        self._si_process_simple_fields(so_vals)
        self._si_process_m2os(so_vals)
        self._si_simulate_onchanges(so_vals)
        return so_vals

    def _si_process_simple_fields(self, so_vals):
        # TODO actually use these fields
        del so_vals["payment_mode"]
        del so_vals["transaction_id"]
        del so_vals["status"]

    def _si_process_m2os(self, so_vals):
        partner_id = self._si_get_partner(so_vals)
        self._si_process_addresses(partner_id, so_vals)
        self._si_process_lines(so_vals)
        self._si_process_amount(so_vals)
        self._si_process_invoice(so_vals)
        self._si_process_sale_channel(so_vals)
        self._si_process_currency_code(so_vals)

    def _si_get_partner(self, so_vals):
        email = so_vals.get("address_customer") and so_vals.get("address_customer").get(
            "email"
        )
        partner = self.env["res.partner"].search([("email", "=", email)])
        if not partner:
            raise ValidationError(_("No customer found"))
        return partner

    def _si_process_addresses(self, partner_id, so_vals):
        # customer itself
        vals_addr_customer = so_vals["address_customer"]
        partner_id.state_id = (
            self.env["res.country.state"]
            .search([("code", "=", vals_addr_customer["state_code"])])
            .id
        )
        partner_id.country_id = (
            self.env["res.country"]
            .search([("code", "=", vals_addr_customer["country_code"])])
            .id
        )
        for field in MAPPINGS_SALE_ORDER_ADDRESS_SIMPLE:
            new_val = vals_addr_customer.get(field)
            if new_val:
                setattr(partner_id, field, new_val)
        so_vals["partner_id"] = partner_id.id
        del so_vals["address_customer"]

        # invoice and shipping: find or create partner based on values
        res_partner_obj = self.env["res.partner"]
        vals_addr_invoicing = so_vals["address_invoicing"]
        vals_addr_shipping = so_vals["address_shipping"]
        for address_field in (
            (vals_addr_shipping, "partner_shipping_id", "address_shipping"),
            (vals_addr_invoicing, "partner_invoice_id", "address_invoicing"),
        ):
            addr = address_field[0]
            field = address_field[1]
            vals_key = address_field[2]
            addr["state_id"] = self.env["res.country.state"].search(
                [("code", "=", addr["state_code"])]
            )
            del addr["state_code"]
            addr["country_id"] = self.env["res.country"].search(
                [("code", "=", addr["country_code"])]
            )
            del addr["country_code"]
            addr["parent_id"] = partner_id
            res_partner_virtual = res_partner_obj.new(addr)
            # on create res.partner Odoo rewrites address values to be the
            # same as the parent's, thus we force set to our values
            for k, v in addr.items():
                setattr(res_partner_virtual, k, v)
            version = res_partner_virtual.get_address_version()
            so_vals[field] = version.id
            del so_vals[vals_key]

    def _si_process_lines(self, so_vals):
        lines = so_vals["lines"]
        so_vals["order_line"] = list()
        for line in lines:
            product_id = (
                self.env["product.product"]
                .search([("default_code", "=", line["product_code"])])
                .id
            )
            qty = line["qty"]
            price_unit = line["price_unit"]
            description = line["description"]
            discount = line["discount"]
            line_vals_dict = {
                "product_id": product_id,
                "product_uom_qty": qty,
                "price_unit": price_unit,
                "name": description,
                "discount": discount,
            }
            line_vals_command = (0, 0, line_vals_dict)
            so_vals["order_line"].append(line_vals_command)
        del so_vals["lines"]

    def _si_process_amount(self, so_vals):
        for k, v in so_vals["amount"].items():
            si_key = "si_" + k
            so_vals[si_key] = v
        del so_vals["amount"]

    def _si_process_invoice(self, so_vals):
        # TODO actually use that val
        del so_vals["invoice"]

    def _si_process_currency_code(self, so_vals):
        # TODO actually use that val
        del so_vals["currency_code"]

    def _si_process_sale_channel(self, so_vals):
        channel = self.env["sale.channel"].search(
            [("name", "=", so_vals.get("sale_channel"))]
        )
        if channel:
            so_vals["sale_channel_id"] = channel.id
            del so_vals["sale_channel"]

    def _si_simulate_onchanges(self, order):
        """ Drawn from connector_ecommerce module
        Play the onchange of the sales order and it's lines
        :param order: sales order values
        :type: dict
        :param order_lines: data of the sales order lines
        :type: list of dict
        :return: the sales order updated by the onchanges
        :rtype: dict
        """
        order_onchange_fields = [
            "partner_id",
            "partner_shipping_id",
            "payment_mode_id",
            "workflow_process_id",
        ]

        line_onchange_fields = ["product_id"]

        # play onchange on sales order
        order = self._si_simulate_onchanges_play_onchanges(
            "sale.order", order, order_onchange_fields
        )

        # play onchange on sales order line
        processed_order_lines = []
        line_lists = [order["order_line"]]

        for line_list in line_lists:
            for idx, command_line in enumerate(line_list):
                # line_list format:[(0, 0, {...}), (0, 0, {...})]
                if command_line[0] in (0, 1):  # create or update values
                    # keeps command number and ID (or 0)
                    old_line_data = command_line[2]
                    new_line_data = self._si_simulate_onchanges_play_onchanges(
                        "sale.order.line", old_line_data, line_onchange_fields
                    )
                    new_line = (command_line[0], command_line[1], new_line_data)
                    processed_order_lines.append(new_line)
                    # in place modification of the sales order line in the list
                    line_list[idx] = new_line
        return order

    def _si_simulate_onchanges_play_onchanges(self, model, values, onchange_fields):
        model = self.env[model]
        onchange_specs = model._onchange_spec()

        # we need all fields in the dict even the empty ones
        # otherwise 'onchange()' will not apply changes to them
        all_values = values.copy()
        for field in model._fields:
            if field not in all_values:
                all_values[field] = False

        # we work on a temporary record
        new_record = model.new(all_values)

        new_values = {}
        for field in onchange_fields:
            onchange_values = new_record.onchange(all_values, field, onchange_specs)
            new_values.update(
                self._si_simulate_onchanges_get_new_values(
                    values, onchange_values, model=model._name
                )
            )
            all_values.update(new_values)

        res = {f: v for f, v in all_values.items() if f in values or f in new_values}
        return res

    def _si_simulate_onchanges_get_new_values(
        self, record, on_change_result, model=None
    ):
        vals = on_change_result.get("value", {})
        new_values = {}
        for fieldname, value in vals.items():
            if not record.get(fieldname):  # fieldname not in record:
                if model:
                    column = self.env[model]._fields[fieldname]
                    if column.type == "many2one":
                        value = value[0]  # many2one are tuple (id, name)
                new_values[fieldname] = value
        return new_values

    # FINALIZERS
    def _si_finalize(self, new_sale_order, raw_import_data):
        """ Extend to add final operations """
        self._si_create_sale_channel_binding(new_sale_order, raw_import_data)
        new_sale_order.si_exc_check_amounts_total = True
        new_sale_order.si_exc_check_amounts_untaxed = True
        self._si_create_payment(raw_import_data)

    def _si_create_sale_channel_binding(
        self, sale_order, data
    ):  # todo on créé un binding à chaque sale order ou on
        # créé que si ça n'existe pas ?
        binding_vals = {
            "sale_channel_id": sale_order.sale_channel_id.id,
            "partner_id": sale_order.partner_id.id,
            "external_id": data["address_customer"]["external_id"],
            "sale_order_id": sale_order.id,  # todo remove ?
        }
        self.env["res.partner.binding"].create(binding_vals)

    def _si_create_payment(self, raw_import_data):
        pass  # todo
