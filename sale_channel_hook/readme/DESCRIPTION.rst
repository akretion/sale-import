This module adds hooks to sales channels for further customization by other modules.

To use, customize your sales channel with the information necessary to make a request, then
implement on sales channel a _get_hook_content_<your_event> function, then call execute_hook(<your_event>, args).
