from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import uuid
import os

# Create your models here.
def file_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}{1}'.format(uuid.uuid4(), os.path.splitext(filename)[-1])

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index = True)
    file = models.FileField(upload_to = file_path)
    filename = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now=True)
    classify = models.CharField(max_length=128, blank=True)
    face = models.FileField(upload_to = file_path, blank=True)

@receiver(pre_delete)
def callback(sender, **kwargs):
    if sender == Record:
        instance = kwargs['instance']
        os.remove(instance.file.path)
        if os.path.exists(instance.face.path):
            os.remove(instance.face.path)
        