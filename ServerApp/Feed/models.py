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
        return self.title
