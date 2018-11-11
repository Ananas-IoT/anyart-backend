from django.urls import path

from upload.views import PhotoUploadViewSet


urlpatterns = [
    path('photo_upload/', PhotoUploadViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('photo_upload/<int:pk>', PhotoUploadViewSet.as_view({'get': 'retrieve'}))
]