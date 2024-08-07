from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("<int:pk>/profile/", views.GetUpdateContactView.as_view()),
    path("<int:pk>/user/", views.GetUserInfo.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
