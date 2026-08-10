from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            'id',
            'full_name',
            'email',
            'phone',
            'subject',
            'message',
            'is_read',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        if not attrs.get('full_name'):
            raise serializers.ValidationError({'full_name': 'Full name is required.'})
        if not attrs.get('email'):
            raise serializers.ValidationError({'email': 'Email is required.'})
        if not attrs.get('phone'):
            raise serializers.ValidationError({'phone': 'Phone number is required.'})
        if not attrs.get('message'):
            raise serializers.ValidationError({'message': 'Message is required.'})
        return attrs
