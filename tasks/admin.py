from django.contrib import admin
from .models import Contact
# Register your models here.

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('cinema/css/admin.css',)
        }
        js = ("cinema/js/admin.js",)
        