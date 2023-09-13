from django.db import models

# Create your models here.

class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='uploads/')
