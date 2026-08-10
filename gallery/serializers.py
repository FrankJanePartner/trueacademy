from rest_framework import serializers

from .models import GalleryCategory, GalleryImage, validate_gallery_image


class GalleryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'slug']


class GalleryImageSerializer(serializers.ModelSerializer):
    # Read: returns nested category object  {id, name, slug}
    # Write: accepts category PK integer
    category = GalleryCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=GalleryCategory.objects.all(),
        source='category',
        write_only=True,
        required=True,
    )
    image = serializers.ImageField(write_only=True, required=False)
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
            'category_id',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'image_url', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if not obj.image:
            return ''
        try:
            return obj.image.url
        except Exception:
            return ''

    def validate(self, attrs):
        if self.instance is None and 'image' not in attrs:
            raise serializers.ValidationError({'image': 'An image is required when creating a gallery item.'})
        if not attrs.get('year'):
            from django.utils import timezone
            attrs['year'] = timezone.now().year
        return attrs

    def validate_image(self, value):
        try:
            validate_gallery_image(value)
        except Exception as exc:
            raise serializers.ValidationError(exc.messages if hasattr(exc, 'messages') else str(exc)) from exc

        return value

    def validate_year(self, value):
        if value < 2000 or value > 2100:
            raise serializers.ValidationError('Year must be between 2000 and 2100.')
        return value
