from django.urls import path

from upload.views import PhotoUploadViewSet, PhotoUploadListView

detail_map = PhotoUploadViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('photo_upload/', PhotoUploadViewSet.as_view({'post': 'create'})),
    path('photo_upload/all/', PhotoUploadListView.as_view()),
    path('photo_upload/<int:id>', detail_map)
]