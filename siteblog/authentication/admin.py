from django.contrib import admin
from .models import *
class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("username",)}

admin.site.register(User, UserAdmin)
# Register your models here.
