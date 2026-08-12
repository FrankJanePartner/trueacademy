from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'id',
            'full_name',
            'phone',
            'email',
            'location',
            'involvement',
            'experience',
            'interests',
            'challenge',
            'attend_all',
            'ethics_commitment',
            'heard_from',
            'refer_friends',
            'referral_numbers',
            'cohort',
            'status',
            'submitted_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'submitted_at', 'updated_at']

    def create(self, validated_data):
        return Application.objects.create(**validated_data)
