This module adds hooks to sales channels for further customization by other modules.

To use, let's take for example:

* We want to make an API call whenever some event happens, we will call the trigger MY_EVENT

* On your sale order: extend some function to call trigger_hook(MY_EVENT, hook_content). Next,
  implement _get_hook_content_MY_EVENT(hook_content)

* On sale channel: add a field hook_active_MY_EVENT. This will enable or disable the hook

* Finally, in the DB: fill necessary information on your sale channel so that it knows which route to call and which token to use,
  and if we actually want to use the MY_EVENT hook for that particular channel
