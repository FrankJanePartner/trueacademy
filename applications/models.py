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
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    location = models.CharField(max_length=255, blank=True)

    involvement = models.CharField(max_length=100, blank=True)
    experience = models.CharField(max_length=100, blank=True)
    interests = models.JSONField(blank=True, null=True)
    challenge = models.TextField(blank=True)

    attend_all = models.CharField(max_length=50, blank=True)
    ethics_commitment = models.CharField(max_length=50, blank=True)

    heard_from = models.CharField(max_length=100, blank=True)
    refer_friends = models.CharField(max_length=50, blank=True)
    referral_numbers = models.TextField(blank=True)

    cohort = models.CharField(max_length=100, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'cohort'],
                name='unique_application_per_email_cohort'
            )
        ]

    def __str__(self):
        return f"{self.full_name} ({self.email}) - {self.cohort}"
