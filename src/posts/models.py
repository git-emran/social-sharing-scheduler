from django.db import models
from django.conf import settings
from django.utils import timezone


User = settings.AUTH_USER_MODEL
print(User)


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    share_on_linkedin = models.BooleanField(default=False)
    shared_at_linkedin = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # pre-save
        if self.share_on_linkedin:
            print("sharing on linked")
            self.shared_at_linkedin = timezone.now()
        super().save(*args, **kwargs)
        # post-save
