This module adds hooks to sales channels for further customization by other modules.

To use, let's take for example:

* We want to make an API call whenever some event happens, we will call the trigger MY_EVENT

* On your sale order: extend some function to call trigger_hook(MY_EVENT, hook_content). Next,
  implement _get_hook_content_MY_EVENT(hook_content)

* On sale channel: add a field hook_active_MY_EVENT. This will enable or disable the hook

* Finally, in the DB: fill necessary information on your sale channel so that it knows which route to call and which token to use,
  and if we actually want to use the MY_EVENT hook for that particular channel

* Use server environment functionality to securely store your API key.
  Either set it in your config file like:

  [sale_channel.Amazon]

  api_key=MySecureApiKey

  or use server_environment_files


A note on how to use the API keys:

A channel's API key is the secret used to calculate the payload signature hash. Both the sending server (Odoo server) and
receiving server must have the same secret API key.

When you receive a hook's payload, you must verify its provenance by doing so:

- Get the payload's contents
- Encrypt the contents in utf-8 using SHA256 using the secret as key, this will give
  you the request's hash. See _generate_hook_request_signature for python implementation.
- Compare the request's signature hash with your own calcuated hash
