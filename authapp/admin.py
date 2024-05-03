from django.contrib import admin
from authapp.models import CustomUser, Lead, Task


admin.site.register(CustomUser)
admin.site.register(Lead)
admin.site.register(Task)
