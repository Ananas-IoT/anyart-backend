from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('auth/', include('authorization.urls'), name='auth'),
    path('approval/', include('approval.urls'), name='approval'),
    path('map/', include('map.urls'), name='map'),
    path('upload/', include('upload.urls'), name='upload'),
    path('voting/', include('voting.urls'), name='voting'),
]