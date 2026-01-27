from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


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

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if len(self.content) < 5:
            raise ValidationError({"content": "This is Invalid"})
        elif self.share_on_linkedin and not self.can_share_on_linkedin:
            raise ValidationError({"content": "Content already shared on linkedin"})

    def save(self, *args, **kwargs):
        # pre-save
        if self.share_on_linkedin and self.can_share_on_linkedin:
            print("sharing on linked")
            self.shared_at_linkedin = timezone.now()
        else:
            print("not sharing on linkedin")
        super().save(*args, **kwargs)
        # post-save

    @property
    def can_share_on_linkedin(self):
        return not self.share_on_linkedin
