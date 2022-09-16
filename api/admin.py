from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ['pk', 'public_id', 'refresh']


admin.site.register(Client, ClientAdmin)
