from django.contrib import admin

# Register your models here.
from common.models import CustomUser, Team
admin.site.register(CustomUser)
admin.site.register(Team)
