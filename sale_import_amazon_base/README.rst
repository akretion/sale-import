=====================
Amazon Connector Base
=====================

Base module to create Sale Orders from Amazon with the SP-API.

There is two way to sell products with Amazon :

- A *Seller* use the Amazon platform to sell and ship product directly to the customer
- A *Vendor* sell products to Amazon, answering Amazon's Purchase Orders.

This base module only create the Marketplace model and fields for credentials, which are used in both modules *sale_import_amazon_seller* and *sale_import_amazon_vendor*

Configuration
=============

To avoid storing your credentials in database, you can define them in the configuration files of your "server_environment_files" module as following::

	[sale_channel.Amazon]
	lwa_appid = XXXX
	sp_api_refresh_token = YYYY
	lwa_client_secret = ZZZZ

You can use the ``server_environment_data_encryption`` module if you want these configuration files to be encrypted.

Check OCA's module `server_environment <https://github.com/OCA/server-env/tree/16.0/server_environment>`_ for more info.

