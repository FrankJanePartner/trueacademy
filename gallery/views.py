from rest_framework import generics, permissions, parsers
from .models import GalleryImage
from .serializers import GalleryImageSerializer


class GalleryImageListCreateView(generics.ListCreateAPIView):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = GalleryImage.objects.filter(is_active=True)
        year = self.request.query_params.get('year')
        category = self.request.query_params.get('category')
        if year:
            queryset = queryset.filter(year=year)
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class GalleryImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        if self.request.method == 'GET':
            return GalleryImage.objects.filter(is_active=True)
        return GalleryImage.objects.all()
