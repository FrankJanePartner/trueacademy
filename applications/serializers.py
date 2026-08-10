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
        read_only_fields = ['id', 'updated_at']

    def validate_interests(self, value):
        if not isinstance(value, list) or len(value) == 0:
            raise serializers.ValidationError('At least one interest must be selected.')
        return value

    def validate(self, attrs):
        if not attrs.get('full_name'):
            raise serializers.ValidationError({'full_name': 'Full name is required.'})
        if not attrs.get('phone'):
            raise serializers.ValidationError({'phone': 'Phone number is required.'})
        if not attrs.get('email'):
            raise serializers.ValidationError({'email': 'Email is required.'})
        if not attrs.get('location'):
            raise serializers.ValidationError({'location': 'City / State is required.'})
        if not attrs.get('challenge'):
            raise serializers.ValidationError({'challenge': 'Biggest challenge is required.'})
        if not attrs.get('submitted_at'):
            raise serializers.ValidationError({'submitted_at': 'Submission time is required.'})
        if not attrs.get('cohort'):
            raise serializers.ValidationError({'cohort': 'Cohort is required.'})
        return attrs

    def create(self, validated_data):
        return Application.objects.create(**validated_data)
