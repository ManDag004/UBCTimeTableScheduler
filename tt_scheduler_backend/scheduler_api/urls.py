from django.urls import path
from .views import CourseListView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
]
