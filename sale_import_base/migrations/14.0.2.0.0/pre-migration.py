# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.column_exists(env.cr, "payment_acquirer", "ref"):
        # in v16
        # payment_acquirer is renamed payment_provider
        # and there is another different "code" field on payment_provider
        # in sale_import_base (v16) the code field is now ref
        # but without migration script
        # therefore, we change it here to be future proof.
        openupgrade.rename_fields(
            env,
            [
                (
                    "payment.aquirer",
                    "payment_acquirer",
                    "code",
                    "ref",
                ),
            ],
        )
