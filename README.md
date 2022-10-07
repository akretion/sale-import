[![Runbot Status](https://runbot.odoo-community.org/runbot/badge/flat//12.0.svg)](https://runbot.odoo-community.org/runbot/repo/github-com-oca-sale-import-)
[![Build Status](https://travis-ci.com/OCA/sale-import.svg?branch=12.0)](https://travis-ci.com/OCA/sale-import)
[![codecov](https://codecov.io/gh/OCA/sale-import/branch/12.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-import)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-import-12-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-import-13-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# sale-import

Set of modules to manage Sale Order imports through a JSON API

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[queue_job_chunk](queue_job_chunk/) | 14.0.1.0.1 |  | Job Queue Chunk
[sale_channel](sale_channel/) | 14.0.1.0.0 |  | Adds the notion of sale channels
[sale_channel_hook](sale_channel_hook/) | 14.0.1.0.0 |  | Adds customizable hooks to the sale channel
[sale_channel_hook_delivery_done](sale_channel_hook_delivery_done/) | 14.0.1.0.0 |  | Adds a hook for when a Sale Order is marked as delivered
[sale_channel_hook_invoice](sale_channel_hook_invoice/) | 14.0.1.0.0 |  | Adds a hook for when a sale order emits an invoice
[sale_channel_hook_sale_state](sale_channel_hook_sale_state/) | 14.0.1.0.0 |  | Adds a hook for when a sale order emits an invoice
[sale_channel_hook_stock_variation](sale_channel_hook_stock_variation/) | 14.0.1.0.0 |  | On stock variation, trigger notification to external webservice
[sale_channel_partner](sale_channel_partner/) | 14.0.1.0.0 |  | Bind sale channels to contacts
[sale_channel_product](sale_channel_product/) | 14.0.1.0.0 |  | Link Product with sale channel
[sale_channel_white_label](sale_channel_white_label/) | 14.0.1.0.0 |  | Base for white label management
[sale_import_base](sale_import_base/) | 14.0.1.0.0 |  | Base for importing Sale Orders through a JSON file format
[sale_import_delivery_carrier](sale_import_delivery_carrier/) | 14.0.1.0.0 |  | Adds delivery carrier functionality to Sale Imports
[sale_import_rest](sale_import_rest/) | 14.0.1.0.1 |  | REST API for importig Sale Orders

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to OCA
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----

OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.
