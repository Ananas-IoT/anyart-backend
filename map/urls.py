from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from map.views import LocationViewSet, LimitationViewSet, WorkloadViewSet, PhotoUploadViewSet, SketchViewSet

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
    'post': 'add_limitation',
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
    }), name='workload-list'),
    path('workload/<int:pk>/', WorkloadViewSet.as_view({
        'delete': 'destroy',
        'get': 'retrieve',
        'put': 'update'
    }), name='workload-detail'),
    path('photo_upload/', PhotoUploadViewSet.as_view({
        'post': 'create',
        'get': 'get_all'
    }), name='photo_upload-list'),
    path('photo_upload/<int:pk>/', PhotoUploadViewSet.as_view({
        'get': 'get_by_id',
        'delete': 'destroy',
        'put': 'update'
    }), name='photo_upload-detail'),
    path('sketch/', SketchViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='sketch-list'),
    path('sketch/<int:pk>/', SketchViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update'
    }), name='sketch-detail')
])



