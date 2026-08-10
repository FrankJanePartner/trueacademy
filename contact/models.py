from django.db import models


class ContactMessage(models.Model):
    STATUS_NEW = 'new'
    STATUS_READ = 'read'
    STATUS_REPLIED = 'replied'
    STATUS_ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_READ, 'Read'),
        (STATUS_REPLIED, 'Replied'),
        (STATUS_ARCHIVED, 'Archived'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} <{self.email}> - {self.subject or 'Contact'}"
