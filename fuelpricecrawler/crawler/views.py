from fuelpricecrawler.views import (BaseAPIView, APIResponse ,SUCCESS, FAIL,)


class HomeAPIView(BaseAPIView):
    def get(self, request):
        return APIResponse(SUCCESS, message="Welcome, Fuel price crawler is ready to work.")
