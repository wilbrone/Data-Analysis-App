import os
from django.conf import settings
from django import forms
from ..models import UploadedFile

def list_media_files():
    # Define the media root directory
    media_root = settings.MEDIA_ROOT

    # Get a list of all files in the media directory
    files = [f for f in os.listdir(media_root) if os.path.isfile(os.path.join(media_root, f))]

    return files


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('file_name', 'file_path')