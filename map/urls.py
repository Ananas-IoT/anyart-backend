from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from map.views import LocationViewSet, LimitationViewSet, WorkloadViewSet, PhotoUploadViewSet

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
map_location_restrictions = LocationViewSet.as_view({
    'get': 'get_limitations',
    'post': 'add_limitations',
})
limitation_list = LimitationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
limitation_detail = LimitationViewSet.as_view({
    'get': 'get',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('locations/', map_list, name='map-list'),
    path('locations/<int:pk>/', map_detail, name='map-detail'),
    path('locations/<int:pk>/limitations/', map_location_restrictions, name='map-limitations'),
    path('limitations/', limitation_list, name='limitation_list'),
    path('limitations/<int:pk>/', limitation_detail, name='limitation-detail'),
    path('workload/', WorkloadViewSet.as_view({
        'post': 'create',
        'get': 'list'
    })),
    path('photo_upload/', PhotoUploadViewSet.as_view({
        'post': 'create',
        'get': 'get_all'
    })),
    path('photo_upload/<int:pk>/', PhotoUploadViewSet.as_view({
        'get': 'get_by_id',
        'delete': 'destroy',
        'put': 'update'
    }))
])



