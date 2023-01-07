from django.db import models
import datetime

# Create your models here.
class Todo(models.Model):
    task = models.CharField(max_length=120, blank=False, null=False)
    deadline = models.DateField(default=datetime.date.today, blank=False, null=False)
    is_complete = models.BooleanField(default=False)
    is_overdue = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.task
    