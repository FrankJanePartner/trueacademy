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
        full_name = (attrs.get('full_name') or '').strip()
        email = (attrs.get('email') or '').strip()
        phone = (attrs.get('phone') or '').strip()
        message = (attrs.get('message') or '').strip()
        subject = (attrs.get('subject') or '').strip()

        if not full_name:
            raise serializers.ValidationError({'full_name': 'Full name is required.'})
        if not email:
            raise serializers.ValidationError({'email': 'Email is required.'})
        if not phone:
            raise serializers.ValidationError({'phone': 'Phone number is required.'})
        if not message:
            raise serializers.ValidationError({'message': 'Message is required.'})

        attrs['full_name'] = full_name
        attrs['email'] = email
        attrs['phone'] = phone
        attrs['subject'] = subject
        attrs['message'] = message
        return attrs

