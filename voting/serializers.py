from rest_framework import serializers

from voting.models import UserVote, GovernmentVote


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserVote
        fields = ('vote', )


class GovernmentVoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GovernmentVote
        fields = ('vote', 'timestamp')

