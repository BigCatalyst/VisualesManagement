from django import forms
from django.db.models import Avg, Case, F, FloatField, Value, When
from django.db.models import Q
from django.db import models
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget, FilteredSelectMultiple
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from movie.admin import AdminImageWidget
from django.utils.safestring import mark_safe


from serial.models import Season, Serial


class SerialResource(resources.ModelResource):
    class Meta:
        model = Serial
        exclude = ["imdb", "film_affinity", "reviewed"]
        
    @staticmethod
    def dehydrate_gender(instance):   
        return '%s' % instance.gender.name
        
    @staticmethod
    def dehydrate_actor(instance):   
        return '%s' % ", ".join(instance.actor.all().values_list("name", flat=True))


class SeasonInlineAdmin(admin.StackedInline):
    model = Season
    extra = 1
    

class SerialModelForm(forms.ModelForm):
    c = tuple([("", "Seleccione un tipo de programa".center(52, '-'))] + [(value, value) for value in set(Serial.objects.values_list("type", flat=True))])    
    type = forms.ChoiceField(widget=forms.Select, choices=c, initial="", label="Tipo")
    class Meta:
        model = Serial
        fields = "__all__" 

class Novela(Serial):
    class Meta:
        proxy = True
        verbose_name = u"Novela"
        
@admin.register(Serial)
class SerialModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_actor" data-href-template="/admin/serial/serial/%s/change/" href="/admin/serial/serial/%s/change/"" title="Cambiar Serie seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Serie seleccionada/o" href="/admin/serial/serial/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True

    exclude = ["imdb", "film_affinity", "reviewed", "initial"]
    list_display = ["type", "title", "title_eng", "gender", "synopsis", "origen", "photo",  opciones]
    list_display_links = ["title_eng"]
    filter_horizontal = ["actor"]
    search_fields = ["title_eng", "title"]
    resource_class = SerialResource
    form = SerialModelForm

    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}, models.TextField: {'widget': forms.Textarea(attrs={'cols':38, "style":"margin: 0px 0px 2px; width: 1056px; height: 137px;"})}}
    inlines = [SeasonInlineAdmin]
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('title',),('title_eng',),('type',),('gender',),('origen',),("in_transmission"),("actor",),('synopsis',)
                ),
                "classes": ("games",)
            }
        ), 
    )
    
    class Media:
        css = {
            'all': ('cinema/css/admin.css',)
        }
        js = ("cinema/js/admin.js",)
        
    def get_queryset(self, request):
        qs = super().get_queryset(request).exclude(Q(type="Novela")).order_by("title_eng")
        if "q" in request.GET:
            search_term = request.GET.get("q", "")
            qs = qs.annotate(
                k1=Case(
                    When(title_eng__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(title_eng__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k3=Case(
                    When(title__istartswith=search_term, then=Value(1)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k4=Case(
                    When(title__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k5=Case(
                    When(actor__name__istartswith=search_term, then=Value(1)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k6=Case(
                    When(actor__name__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                rank=F("k1") + F("k2"),
                rank2=F("k3") + F("k4"),
                rank3=F("k5") + F("k6")
                
            ).exclude(Q(rank=0.0) & Q(rank2=0.0) & Q(rank3=0.0)).distinct().order_by("-rank", "-rank2", "-rank3", "title_eng")
        else:
            self.ordering = ["title_eng"]
        return qs
    
        
@admin.register(Novela)
class NovelaModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_actor" data-href-template="/admin/serial/serial/%s/change/" href="/admin/serial/novela/%s/change/"" title="Cambiar Serie seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Serie seleccionada/o" href="/admin/serial/novela/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True

    exclude = ["imdb", "film_affinity", "reviewed", "initial"]
    list_display = ["type", "title", "title_eng", "gender", "synopsis", "origen", "photo",  opciones]
    list_display_links = ["title_eng"]
    filter_horizontal = ["actor"]
    search_fields = ["title_eng", "title"]
    resource_class = SerialResource
    form = SerialModelForm
    
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}, models.TextField: {'widget': forms.Textarea(attrs={'cols':38, "style":"margin: 0px 0px 2px; width: 1056px; height: 137px;"})}}
    inlines = [SeasonInlineAdmin]
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('title',),('title_eng',),('type',),('gender',),('origen',),("in_transmission"),("actor",),('synopsis',)
                ),
                "classes": ("games",)
            }
        ), 
    )
    
    class Media:
        css = {
            'all': ('cinema/css/admin.css',)
        }
        js = ("cinema/js/admin.js",)
        
    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(Q(type="Novela")).order_by("title_eng")
        if "q" in request.GET:
            search_term = request.GET.get("q", "")
            qs = qs.annotate(
                k1=Case(
                    When(title_eng__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(title_eng__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k3=Case(
                    When(title__istartswith=search_term, then=Value(1)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k4=Case(
                    When(title__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k5=Case(
                    When(actor__name__istartswith=search_term, then=Value(1)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k6=Case(
                    When(actor__name__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                rank=F("k1") + F("k2"),
                rank2=F("k3") + F("k4"),
                rank3=F("k5") + F("k6")
                
            ).exclude(Q(rank=0.0) & Q(rank2=0.0) & Q(rank3=0.0)).distinct().order_by("-rank", "-rank2", "-rank3", "title_eng")
            print(qs)
        else:
            self.ordering = ["title_eng"]
        return qs

@admin.register(Season)
class SeasonModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).order_by("number")
