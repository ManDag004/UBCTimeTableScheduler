from rest_framework.views import APIView
from rest_framework.response import Response
from .model.main import find_schedule

class CourseListView(APIView):
    def post(self, request):
        print(f"started with {request.data.get('search_params')}")
        criteria = request.data.get('search_params')
        course_names = criteria.get('courseNames')
        term = int(criteria.get('term'))
        min_start_time = criteria.get('minStartTime')
        max_end_time = criteria.get('maxEndTime')

        return Response(find_schedule(course_names, term, min_start_time, max_end_time))

