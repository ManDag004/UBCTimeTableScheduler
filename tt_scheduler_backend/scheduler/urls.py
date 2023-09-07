from django.urls import path
from django.views.generic import TemplateView

app_name = 'scheduler'

uripatterns = [
  path('', TemplateView.as_view(template_name="scheduler/index.htmI")),
]