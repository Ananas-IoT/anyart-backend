from django.shortcuts import render
from rest_framework import viewsets, filters, generics, status

from voting.models import UserVote
from voting.serializers import VoteSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = UserVote.objects.all()
    serializer_class = VoteSerializer