from django.contrib import admin
from .models import Offer, CodeExample, Domain, RootDomain, SubDomain, OfferPosition, CopyPaste, CopyPasteData, \
    Country, DomCamp, Spend


# Register your models here.

class CodeExampleAdmin(admin.ModelAdmin):
    list_display = ['name']


class DomainAdmin(admin.ModelAdmin):
    list_display = ['id', 'beget_id', 'name', ]
    list_display_links = ['name']
    search_fields = ['name']


class RootDomainAdmin(admin.ModelAdmin):
    list_display = ['id', 'beget_id', 'name', 'is_full',]
    list_display_links = ['name']
    search_fields = ['name']


class SubDomainAdmin(admin.ModelAdmin):
    list_display = ['id', 'beget_id', 'name', ]
    list_display_links = ['name']
    search_fields = ['name']

class PopyPasteAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_display_links = ['name']

class CopyPasteDataAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'data']
    list_display_links = ['name']


admin.site.register(Offer)
admin.site.register(CodeExample)
admin.site.register(Domain, DomainAdmin)
admin.site.register(RootDomain, RootDomainAdmin)
admin.site.register(SubDomain, SubDomainAdmin)
admin.site.register(CopyPaste, PopyPasteAdmin)
admin.site.register(OfferPosition)
admin.site.register(CopyPasteData, CopyPasteDataAdmin)
admin.site.register(Country)
admin.site.register(DomCamp)
admin.site.register(Spend)
