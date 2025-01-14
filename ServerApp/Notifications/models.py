from django.db import models

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # sender_id = models.CharField(max_length=100, default='')
    # recipient_ids = models.JSONField(default=list)

    def __str__(self):
        return {
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            # "sender_id": self.sender_id,
            # "recipient_ids": self.recipient_ids
        }
