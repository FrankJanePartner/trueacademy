from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageListCreateView(generics.ListCreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'OPTIONS']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact_msg = serializer.save(is_read=False, status=ContactMessage.STATUS_NEW)

        try:
            from django.core.mail import send_mail
            from django.conf import settings
            admin_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@true.academy')
            send_mail(
                subject=f"New Contact Message: {contact_msg.subject or 'No Subject'}",
                message=f"From: {contact_msg.full_name} <{contact_msg.email}>\nPhone: {contact_msg.phone}\n\nMessage:\n{contact_msg.message}",
                from_email=None,
                recipient_list=[admin_email],
                fail_silently=True,
            )
        except Exception:
            pass

        return Response({
            'success': True,
            'message': 'Your message has been received successfully.',
            'data': serializer.data,
        }, status=status.HTTP_201_CREATED)



class ContactMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAdminUser]
