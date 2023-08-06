from django.contrib import admin
from django.contrib.auth.models import User

from .models import Sessions, Messages

# Register your models here.
admin.site.register(Sessions)
admin.site.register(Messages)