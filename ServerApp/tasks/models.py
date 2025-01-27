from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
