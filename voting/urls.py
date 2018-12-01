from django.urls import path

from voting.views import VoteViewSet

generic_dict = VoteViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('vote/', generic_dict)
]