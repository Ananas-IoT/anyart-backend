from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from map.views import LocationViewSet

map_list = LocationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
map_detail = LocationViewSet.as_view({
    'get': 'get',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
map_limitations = LocationViewSet.as_view({
    'get': 'get_limitations',
    'put': 'add_limitations',
})
#urlpatterns = []

urlpatterns = format_suffix_patterns([
    path('maps/', map_list, name='map-list'),
    path('maps/<int:pk>/', map_detail, name='map-detail'),
    path('maps/limitations/<int:pk>/', map_limitations, name='map-limitations'),
])



