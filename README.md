
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/sale-channel&target_branch=16.0)
[![Pre-commit Status](https://github.com/OCA/sale-channel/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-channel/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/OCA/sale-channel/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/OCA/sale-channel/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/OCA/sale-channel/branch/16.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-channel)
[![Translation Status](https://translation.odoo-community.org/widgets/sale-channel-16-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/sale-channel-16-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Module for managing sale channel


Module for managing several sale channel

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[queue_job_chunk](queue_job_chunk/) | 16.0.0.0.0 |  | Job Queue Chunk
[sale_channel](sale_channel/) | 16.0.0.0.0 |  | Adds the notion of sale channels
[sale_channel_partner](sale_channel_partner/) | 16.0.0.0.0 |  | Bind sale channels to contacts
[sale_channel_white_label](sale_channel_white_label/) | 16.0.0.0.0 |  | Base for white label management


Unported addons
---------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_channel_hook](sale_channel_hook/) | 14.0.1.0.0 (unported) |  | Adds customizable hooks to the sale channel
[sale_channel_hook_delivery_done](sale_channel_hook_delivery_done/) | 14.0.1.0.0 (unported) |  | Adds a hook for when a Sale Order is marked as delivered
[sale_channel_hook_invoice](sale_channel_hook_invoice/) | 14.0.1.0.0 (unported) |  | Adds a hook for when a sale order emits an invoice
[sale_channel_hook_sale_state](sale_channel_hook_sale_state/) | 14.0.1.0.0 (unported) |  | Adds a hook for when a sale order emits an invoice
[sale_channel_hook_stock_variation](sale_channel_hook_stock_variation/) | 14.0.1.0.0 (unported) |  | On stock variation, trigger notification to external webservice
[sale_channel_product](sale_channel_product/) | 14.0.1.0.0 (unported) |  | Link Product with sale channel
[sale_import_base](sale_import_base/) | 14.0.1.1.0 (unported) |  | Base for importing Sale Orders through a JSON file format
[sale_import_delivery_carrier](sale_import_delivery_carrier/) | 14.0.1.0.0 (unported) |  | Adds delivery carrier functionality to Sale Imports
[sale_import_rest](sale_import_rest/) | 14.0.1.0.1 (unported) |  | REST API for importig Sale Orders

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.
