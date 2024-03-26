from django.contrib import admin
from authapp.models import CustomUser, Lead


admin.site.register(CustomUser)
admin.site.register(Lead)