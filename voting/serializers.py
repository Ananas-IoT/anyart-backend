from rest_framework import serializers

from voting.models import Vote, GovernmentVote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('user', 'vote', 'timestamp')


class GovernmentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentVote
        fields = ( 'vote', 'timestamp')

