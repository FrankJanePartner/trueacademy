from rest_framework import generics, permissions, parsers

from .models import GalleryCategory, GalleryImage
from .serializers import GalleryCategorySerializer, GalleryImageSerializer


class GalleryCategoryListView(generics.ListAPIView):
    """Public: GET /api/gallery/categories/ — returns active categories."""
    serializer_class = GalleryCategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return GalleryCategory.objects.order_by('name')


class GalleryImageListCreateView(generics.ListCreateAPIView):
    serializer_class = GalleryImageSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        qs = GalleryImage.objects.select_related('category')
        category = self.request.query_params.get('category')  # accepts slug or id
        if category:
            # Support filtering by slug (e.g. ?category=workshop) or by id
            if category.isdigit():
                qs = qs.filter(category_id=int(category))
            else:
                qs = qs.filter(category__slug=category)
        return qs


class GalleryImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GalleryImageSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return GalleryImage.objects.select_related('category')
