from rest_framework import serializers

from voting.models import Vote, GovernmentVote


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ('vote', )


class GovernmentVoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GovernmentVote
        fields = ('vote', 'timestamp')

