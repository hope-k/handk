from rest_framework.response import Response


class ErrorResponse(Response):
    def __init__(self, data=None, status=None, headers=None):
        response_data = {
            'success': False,
            **data
        }
        super().__init__(response_data, status, headers)
