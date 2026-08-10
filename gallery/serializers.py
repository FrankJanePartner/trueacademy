from rest_framework import serializers
from .models import GalleryImage


class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImage
        fields = [
            'id',
            'image',
            'image_url',
            'title',
            'description',
            'year',
            'category',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'image_url', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return obj.image.url
        return request.build_absolute_uri(obj.image.url)

    def validate_image(self, value):
        allowed_types = ['image/jpeg', 'image/png', 'image/webp']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError('Unsupported image type. Use JPG, PNG, or WEBP.')
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Image size must be 5MB or smaller.')
        return value

    def validate_year(self, value):
        if value < 2000 or value > 2100:
            raise serializers.ValidationError('Year must be between 2000 and 2100.')
        return value
