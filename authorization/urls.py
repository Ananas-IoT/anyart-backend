from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from . import views

urlpatterns = [
    path('login/', views.SimpleUserLogin.as_view(template_name='rest_framework/login.html'), name='login'),
    path('logout/', views.SimpleUserLogout.as_view(), name='logout'),
    path('rest-auth/', include('rest_auth.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)