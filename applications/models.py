from django.db import models


class Application(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_REVIEWING = 'reviewing'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_WAITLISTED = 'waitlisted'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_REVIEWING, 'Reviewing'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_WAITLISTED, 'Waitlisted'),
    ]

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    location = models.CharField(max_length=255)
    involvement = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    interests = models.JSONField()
    challenge = models.TextField()
    attend_all = models.CharField(max_length=50)
    ethics_commitment = models.CharField(max_length=50)
    heard_from = models.CharField(max_length=100)
    refer_friends = models.CharField(max_length=50)
    referral_numbers = models.TextField(blank=True)
    cohort = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    submitted_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        unique_together = [['email', 'cohort']]

    def __str__(self):
        return f"{self.full_name} ({self.email}) - {self.cohort}"
