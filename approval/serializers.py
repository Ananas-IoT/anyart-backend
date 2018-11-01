from rest_framework import serializers

from approval.models import CustomLimitation, ApprovalGroup, Veto


class CustomLimitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomLimitation
        fields = ('limitation_name', 'authority_name', 'explanation')


class ApprovalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalGroup
        fields = ('name', 'hierarchy')


class VetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veto
        fields = ('name', 'veto_rank')
