from django.contrib import admin

from .models import ClientDoc


class ClientDocAdmin(admin.ModelAdmin):
    list_display = ['name', 'load_date', 'document_date', 'description', 'document_file']
    exclude = ['document']

admin.site.register(ClientDoc, ClientDocAdmin)
