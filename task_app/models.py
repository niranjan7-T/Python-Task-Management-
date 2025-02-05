from django.db import models
from .enums import *

class Task(models.Model):

    task_id = models.CharField(max_length=10,unique=True,null=True,blank=False)
    description = models.CharField(max_length=255)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[(status.value, status.value) for status in task_state], default=task_state.Pending.value)

    def save(self, *args, **kwargs):
        if not self.id:
            last_application = Task.objects.order_by('-task_id').first()
            if last_application:
                last_id = int(last_application.task_id)
                new_id = str(last_id + 1)
                new_id = f"{new_id.zfill(6)}"
            else:
                new_id = "000001"
            self.task_id = new_id
        super().save(*args, **kwargs)

    