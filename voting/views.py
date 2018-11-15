from django.shortcuts import render
from rest_framework import viewsets, filters, generics, status

from voting.models import Vote
from voting.serializers import VoteSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer