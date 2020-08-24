This module adds hooks to sales channels for further customization by other modules.

To use, let's take for example:

* We want to make an API call when MY_EVENT triggers

* On your object: extend some function to call trigger_hook(MY_EVENT, hook_content),
  where hook_content is whatever you want to pass to the hook function

* On sale channel: implement _get_hook_content_MY_EVENT(hook_content)

* Finally, in the DB: fill necessary information on your sale channel so that it knows which route to call and which token to use,
  and if we actually want to use the MY_EVENT hook for that particular channel
