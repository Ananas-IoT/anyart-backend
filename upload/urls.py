from django.urls import path

from upload.views import PhotoUploadViewSet

detail_dict = PhotoUploadViewSet.as_view({
    'get': 'get_by_id',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

raw_dict = PhotoUploadViewSet.as_view({
    'post': 'create',
    'get': 'get_all'
})

urlpatterns = [
    path('photo_upload/', raw_dict),
    path('photo_upload/<int:id>', detail_dict)
]