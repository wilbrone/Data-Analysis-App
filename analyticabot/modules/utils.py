import os
from django.conf import settings
from django import forms

def list_media_files():
    # Define the media root directory
    media_root = settings.MEDIA_ROOT

    # Get a list of all files in the media directory
    files = [f for f in os.listdir(media_root) if os.path.isfile(os.path.join(media_root, f))]

    return files

def delete_media_file():
    # Define the media root directory
    media_root = settings.MEDIA_ROOT
    user_folder_path = os.path.join(media_root, 'user_id')

    if os.path.exists(user_folder_path):
        files = [f for f in os.listdir(user_folder_path) if os.path.isfile(os.path.join(user_folder_path, f))]
        for file in files:
            file_path = os.path.join(user_folder_path, file)
            os.remove(file_path)
            print(f'Deleted: {file_path}')
    else:
        print('Media folder does not exist.')

    # Delete the file from the media directory
    # os.remove(os.path.join(media_root, filename))

    return
