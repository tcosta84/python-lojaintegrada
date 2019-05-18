class ApiError(Exception):
    def __init__(self, request, response=None):
        self.request = request
        self.response = response
