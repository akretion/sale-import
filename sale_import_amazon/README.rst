================
Connector Amazon
================

Catch Amazon Sale Orders data and created related Odoo Sale Orders

Configuration
=============

To configure this module, you need to:

1. Create a Sale Channel called "Amazon"
2. To avoid storing your credentials in database, you can define them in the configuration files of your "server_environment_files" module as following::

	[sale_channel.Amazon]
	lwa_appid = XXXX
	sp_api_refresh_token = YYYY
	lwa_client_secret = ZZZZ

You can use the ``server_environment_data_encryption`` module if you want these configuration files to be encrypted.

Check OCA's module `server_environment <https://github.com/OCA/server-env/tree/16.0/server_environment>`_ for more info.

Usage
=====

To use this module, you need to:

#. Go to ...


Changelog
=========
