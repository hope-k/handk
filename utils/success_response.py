from rest_framework.response import Response


class SuccessResponse(Response):
    def __init__(self, data=None, status=None, headers=None, exception=False):
        response_data = {
            'success': True,
            **data
        }
        super().__init__(response_data, status, headers, exception)
