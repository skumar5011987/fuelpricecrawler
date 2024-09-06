
from rest_framework.views import APIView, Response, exception_handler

SUCCESS, FAIL=1, 0


class APIResponse(Response):
    def __init__(
        self,
        code,
        data={},
        message=None,
        status=None,
        exception=False,
    ):
        if code is SUCCESS:
            data = {
                "status": SUCCESS,
                "message": message or "ok",
                "data": data,
            }
        else:
            data = {
                "status": FAIL,
                "message": message or "something went wrong",
                "data": {},
            }
        super().__init__(
            data=data,
            status=status,
            exception=exception,
        )


def base_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response."""
    response = exception_handler(exc, context)
    if response is not None:
        errors = []
        for field, value in response.data.items():
            errors.append("{} : {}".format(field, "".join(value)))
        return APIResponse(FAIL, message=", ".join(errors))


class BaseAPIView(APIView):
    
    def get_exception_handler(self):
        """Returns the exception handler that this view uses."""
        
        return base_exception_handler
