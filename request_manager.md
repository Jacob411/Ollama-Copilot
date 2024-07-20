# Request manager to manage scope for request and dropping.
completion is called, it needs to add that request into the queue, and then pull the first valid request in the queue from it.
the queue will be managed, and if the item is out of scope (text changes) it will not be used. 
two methods: add to queue: we add a completion request into our queue with its location and params.

deque (pass in location for current completion, also may need to consider if user has typed over the completion - following or diverging) we grab the first in line, this will be done by checking the requests validity and continuing until valid.
