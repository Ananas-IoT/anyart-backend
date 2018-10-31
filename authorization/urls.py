from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

urlpatterns = [
    path('login/')
]

urlpatterns = format_suffix_patterns(urlpatterns)