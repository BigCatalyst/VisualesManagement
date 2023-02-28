from django import forms
from django.db import models
from django.contrib import admin
from offer.models import Offer
from movie.admin import AdminImageWidget
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin

class OfferResource(resources.ModelResource):
    class Meta:
        model = Offer
        exclude = ["id"] 
        

@admin.register(Offer)
class OfferModelAdmin(ImportExportModelAdmin):#, SummernoteModelAdmin
    def opciones(obj):
        return mark_safe(u'<a id="change_id_actor" data-href-template="/admin/movie/combo/%s/change/" href="/admin/offer/offer/%s/change/" title="Cambiar Oferta seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Oferta seleccionada/o" href="/admin/offer/offer/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    search_fields = ["name","price","type"]
    summernote_fields = ('description',)
    resource_class = OfferResource
    list_display = ["name", "price", "type", "photo",  opciones]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}, models.TextField: {'widget': forms.Textarea(attrs={'cols':38, "style": "width: 276px; height: 32px;"})}}
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('type',), ('price',),('especial',), ('name',), ('description',),
                ),
                "classes": ("games",)
            }
        ), 
    )
    
    class Media:
        css = {
            'all': ('cinema/css/offeradmin.css',)
        }
        js = ("cinema/js/admin.js",)
        

