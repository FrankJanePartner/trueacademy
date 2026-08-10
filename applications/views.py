from django.db import IntegrityError
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Application
from .serializers import ApplicationSerializer


class ApplicationListCreateView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'OPTIONS']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(status=Application.STATUS_PENDING)
        except IntegrityError:
            return Response({
                'success': False,
                'message': 'User already registered for this cohort.',
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'success': True,
            'message': 'Your application has been submitted successfully.',
            'data': serializer.data,
        }, status=status.HTTP_201_CREATED)


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAdminUser]
