
<!-- /!\ Non OCA Context : Set here the badge of your runbot / runboat instance. -->
[![Pre-commit Status](https://github.com/akretion/sale-import/actions/workflows/pre-commit.yml/badge.svg?branch=14.0)](https://github.com/akretion/sale-import/actions/workflows/pre-commit.yml?query=branch%3A14.0)
[![Build Status](https://github.com/akretion/sale-import/actions/workflows/test.yml/badge.svg?branch=14.0)](https://github.com/akretion/sale-import/actions/workflows/test.yml?query=branch%3A14.0)
[![codecov](https://codecov.io/gh/akretion/sale-import/branch/14.0/graph/badge.svg)](https://codecov.io/gh/akretion/sale-import)
<!-- /!\ Non OCA Context : Set here the badge of your translation instance. -->

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
[queue_job_chunk](queue_job_chunk/) | 14.0.1.1.0 |  | Job Queue Chunk
[sale_channel](sale_channel/) | 14.0.1.0.0 |  | Adds the notion of sale channels
[sale_channel_hook](sale_channel_hook/) | 14.0.1.0.0 |  | Adds customizable hooks to the sale channel
[sale_channel_hook_delivery_done](sale_channel_hook_delivery_done/) | 14.0.1.0.0 |  | Adds a hook for when a Sale Order is marked as delivered
[sale_channel_hook_invoice](sale_channel_hook_invoice/) | 14.0.1.0.0 |  | Adds a hook for when a sale order emits an invoice
[sale_channel_hook_sale_state](sale_channel_hook_sale_state/) | 14.0.1.0.0 |  | Adds a hook for when a sale order emits an invoice
[sale_channel_hook_stock_variation](sale_channel_hook_stock_variation/) | 14.0.1.0.0 |  | On stock variation, trigger notification to external webservice
[sale_channel_partner](sale_channel_partner/) | 14.0.1.0.0 |  | Bind sale channels to contacts
[sale_channel_product](sale_channel_product/) | 14.0.1.0.0 |  | Link Product with sale channel
[sale_channel_white_label](sale_channel_white_label/) | 14.0.1.0.0 |  | Base for white label management
[sale_import_base](sale_import_base/) | 14.0.1.1.0 |  | Base for importing Sale Orders through a JSON file format
[sale_import_delivery_carrier](sale_import_delivery_carrier/) | 14.0.1.0.0 |  | Adds delivery carrier functionality to Sale Imports
[sale_import_rest](sale_import_rest/) | 14.0.1.0.1 |  | REST API for importig Sale Orders

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Akretion
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
<!-- /!\ Non OCA Context : Set here the full description of your organization. -->
