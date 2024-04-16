from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from lessons import views

urlpatterns = [
    path("", views.LessonCategoryList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
