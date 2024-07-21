
class RequestManager:
    def __init__(self, max_requests=10):
        # need to have stack for requests
        # need to have recieve didChange events and edit the queue accordingly
        self.requests = []

    def add_request(self, request):
        '''
        Add a request to the request manager
        params:
        request: tuple of (lines, line, character)
        '''
        # if max requests reached, remove the oldest request
        if len(self.requests) >= self.max_requests:
            self.requests.pop(0)
        self.requests.append(request)

    def get_next_request(self):
        '''
        Get the next valid request in the queue
        '''
        pass

    def is_valid_request(self, request):
        '''
        Check if the request is valid
        params:
        request: tuple of (lines, line, character)
        '''
        pass
