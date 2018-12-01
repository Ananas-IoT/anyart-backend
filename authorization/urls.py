from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

from authorization.views import UserViewSet

users_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('users/', users_list, name='users_list'),
    path('registration/', UserViewSet.as_view({'post': 'create'})),
    path('login/', UserViewSet.as_view({'get': 'login'})),
]