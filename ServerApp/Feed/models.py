from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False) # is draft by default
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    document_id = models.CharField(max_length=100, default='') # uid of the document


    def __str__(self):
        return {
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_published": self.is_published,
            "views": self.views,
            "likes": self.likes,
            "document_id": self.document_id
        }
