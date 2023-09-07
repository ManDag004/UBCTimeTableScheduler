from rest_framework.views import APIView
from rest_framework.response import Response
from .model.main import find_schedule

class CourseListView(APIView):
    def post(self, request):
        print(f"started with {request.data.get('search_params')}")
        user_inputs = request.data.get('search_params')

        return Response(find_schedule(user_inputs))

