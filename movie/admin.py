from django import forms
from django.db.models import Avg, Case, F, FloatField, Value, When
from django.db.models import Q
from django.db import models
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget, FilteredSelectMultiple
from django.utils.safestring import mark_safe
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget
from import_export.admin import ImportExportModelAdmin
from django_countries.widgets import CountrySelectWidget
from searchableselect.widgets import SearchableSelect

from actor.models import Actor
from movie.models import (
    Combo,
    ComboMovie,
    Documental,
    DocumentalSeason,
    Format,
    Gender,
    GenderDocumental,
    Humor,
    Movie,
    Sagas,
    Sport,
)

class ListAsQuerySet(list):

    def __init__(self, *args, model, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self  # filter ignoring, but you can impl custom filter

    def order_by(self, *args, **kwargs):
        return self


class ActorResource(resources.ModelResource):
    movies = fields.Field(widget=ManyToManyWidget(Movie))
    series = fields.Field()
    class Meta:
        model = Actor
        fields = ["id", "name", "photo", "movies", "series"]
        export_order = ["id", "name", "photo", "movies", "series"]
    
    @staticmethod
    def dehydrate_movies(instance): 
        if instance.movie_set is not None:
            
            return '%s' % ", ".join([str(id) for id in instance.movie_set.all().values_list("id", flat=True)])
        return ""
    @staticmethod
    def dehydrate_series(instance):  
        if instance.serial_set is not None:
            return '%s' % ", ".join([str(id) for id in instance.serial_set.all().values_list("id", flat=True)])
        return ""

class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        img_id = "form_photo" if name == "photo" else "form_photo_back"
        
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
        else:
            image_url = "/static/cinema/images/benito2.svg"
        file_name = str(value)
        output.append(u' <img src="%s" id="%s" alt="%s"  style="object-fit: contain; width: 300px; height: 280px;"/> ' %(image_url,img_id, file_name))
        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))


@admin.register(Actor)
class ActorModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_actor" data-href-template="/admin/movie/movie/%s/change/" href="/admin/movie/actor/%s/change/" title="Cambiar Actor seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Actor seleccionada/o" href="/admin/movie/actor/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    
    list_display = ["name", "photo", opciones]
    search_fields = ["name"]
    resource_class = ActorResource
    exclude = ["imdb"]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('name',),("display",),
                ),
                "classes": ("games", "alone",)
            }
        ), 
    )
    
    class Media:
        css = {
            'all': ('cinema/css/admin.css',)
        }
        js = ("cinema/js/admin.js",)
        




class MovieResource(resources.ModelResource):
    class Meta:
        model = Movie
        exclude = ["imdb", "film_affinity", "reviewed"]   

    @staticmethod
    def dehydrate_gender(instance):   
        return '%s' % instance.gender.name

    @staticmethod
    def dehydrate_format(instance):   
        return '%s' % instance.format.format
        
    @staticmethod
    def dehydrate_saga(instance):  
        if instance.saga is not None:
            return '%s' % instance.saga.title
        return ""
        
    @staticmethod
    def dehydrate_actor(instance):   
        return '%s' % ", ".join(instance.actor.all().values_list("name", flat=True))

class MovieAdminForm(forms.ModelForm):
    class Meta:
        model = Movie
        
        fields = '__all__' # required for Djan

      

@admin.register(Movie)
class MovieModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_movie" data-href-template="/admin/movie/movie/%s/change/" href="/admin/movie/movie/%s/change/" title="Cambiar Película seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Pelicula seleccionada/o" href="/admin/movie/movie/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    
    list_display = ["title_eng","title", "gender", "photo", "synopsis", "duration", "year", "saga", "format", "origen", "definition", opciones]
    
    form = MovieAdminForm
    exclude = ["imdb", "film_affinity", "reviewed", "initial"]
    list_display_links = ["title_eng"]
    search_fields = ["title_eng", "title", "actor__name"]
    filter_horizontal = ["actor"]
    resource_class = MovieResource
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}, models.TextField: {'widget': forms.Textarea(attrs={'cols':38, "style": "margin: 0px 0px 2px; height: 200px; width: 1015px;"})}}
    fieldsets = (        
        ("",{
                "fields": ( 
                    ('photo',),('title',),("title_eng",), ("gender",), ("sub_gender",),('duration',),("year",), ("origen",), ("format",),
                    ("saga",),('language',),("definition",),("actor",),("synopsis",),
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
        qs = super().get_queryset(request).order_by("title_eng")
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
            ).exclude(Q(rank=0.0) & Q(rank2=0.0) & Q(rank3=0.0)).order_by("-rank", "-rank2", "-rank3", "title_eng", "id").distinct()
                  

        else:
            self.ordering = ["title_eng"]
        return qs
    

class SportResource(resources.ModelResource):
    class Meta:
        model = Sport
        exclude = ["id"] 
        
    @staticmethod
    def dehydrate_format(instance):   
        return '%s' % instance.format.format
        
    
@admin.register(Sport)
class SportModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_actor" data-href-template="/admin/movie/movie/%s/change/" href="/admin/movie/sport/%s/change/" title="Cambiar Deporte seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Deporte seleccionada/o" href="/admin/movie/deporte/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    search_fields = ["name"]
    resource_class = SportResource
    list_display = ["name", "year", "photo", "definition", "format", opciones]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('name',),("year",), ("definition",), ("format",)
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
        qs = super().get_queryset(request).order_by("name")
        if "q" in request.GET:
            search_term = request.GET.get("q", "")
            qs = qs.annotate(
                k1=Case(
                    When(name__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(name__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
               
                rank=F("k1") + F("k2"),
                
            ).exclude(rank=0.0).distinct().order_by("-rank", "name")
        else:
            self.ordering = ["name"]
        return qs    


class DocumentalForm(forms.ModelForm):
    CHOICES = tuple(set([(t.title(),t.title()) if t is not None else ("", "Sin definir") for t in set(Documental.objects.values_list("type", flat=True))]))
    type = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    class Meta:
        model = Documental
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(DocumentalForm, self).__init__(*args, **kwargs)
        self.fields['type'].label = "Tipo"

class DocumentalResource(resources.ModelResource):
    class Meta:
        model = Documental
        exclude = ["id"] 
        
    @staticmethod
    def dehydrate_gender(instance):   
        return '%s' % instance.gender.gender.name

    @staticmethod
    def dehydrate_format(instance):   
        return '%s' % instance.format.format
        
        
class SeasonDocInlineAdmin(admin.StackedInline):
    model = DocumentalSeason 
    extra = 0
    
        
@admin.register(Documental)
class DocumentalModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_actor" data-href-template="/admin/movie/documental/%s/change/" href="/admin/movie/documental/%s/change/" title="Cambiar Documental seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Documental seleccionada/o" href="/admin/movie/documental/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    form = DocumentalForm
    resource_class = DocumentalResource
    search_fields = ["title_eng"]
    list_display = ["title_eng","title", "gender", "photo", "synopsis", "year", "format", opciones]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}, models.TextField: {'widget': forms.Textarea(attrs={'cols':38, "style": "margin: 0px 0px 2px; height: 200px; width: 1015px;"})}}
    inlines = [SeasonDocInlineAdmin]
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('title',),("title_eng",), ("type",), ("gender",),('duration',),("year",),
                    ("origen",),("format",), ("definition",), ('language',), ("synopsis",),
                ),
                "classes": ("games",)
            }
        ), 
    )
    
    class Media:
        css = {
            'all': ('cinema/css/docadmin.css',)
        }
        js = ("cinema/js/admin.js",)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request).order_by("title_eng")
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
                
                rank=F("k1") + F("k2"),
                
            ).exclude(rank=0.0).distinct().order_by("-rank", "title_eng")
        else:
            self.ordering = ["title_eng"]
        return qs    



@admin.register(DocumentalSeason)
class DocumentalSeasonModelAdmin(admin.ModelAdmin):
    pass

class FormatResource(resources.ModelResource):
    class Meta:
        model = Format
        exclude = ["id"] 

@admin.register(Format)
class FormatModelAdmin(ImportExportModelAdmin):
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}, models.TextField: {'widget': forms.Textarea(attrs={'cols':38, "style": "margin: 0px 0px 2px; height: 200px; width: 1015px;"})}}
    resource_class = FormatResource

class GenderDocumentalResource(resources.ModelResource):
    class Meta:
        model = GenderDocumental
        exclude = ["id"]
    

@admin.register(GenderDocumental)
class GenderDocumentalModelAdmin(ImportExportModelAdmin):
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    resource_class = GenderDocumentalResource
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('gender',),("type",),
                ),
                "classes": ("games", "alone",)
            }
        ), 
    )
    
    class Media:
        css = {
            'all': ('cinema/css/adminhumor.css',)
        }
        js = ("cinema/js/admin.js",)

class GenderResource(resources.ModelResource):
    class Meta:
        model = Gender
        exclude = ["id"]

        
@admin.register(Gender)
class GenderModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_actor" data-href-template="/admin/movie/movie/%s/change/" href="/admin/movie/gender/%s/change/" title="Cambiar Género seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Género seleccionada/o" href="/admin/movie/gender/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    source_class = GenderResource
    list_display = ["name", "photo", opciones]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('name',),
                ),
                "classes": ("games", "alone",)
            }
        ), 
    )
    
    class Media:
        css = {
            'all': ('cinema/css/admin.css',)
        }
        js = ("cinema/js/admin.js",)

class HumorResource(resources.ModelResource):
    class Meta:
        model = Humor
        exclude = ["id"]
        

@admin.register(Humor)
class HumorModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_actor" data-href-template="/admin/movie/movie/%s/change/" href="/admin/movie/humor/%s/change/" title="Cambiar Humoristico seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Actor seleccionada/o" href="/admin/movie/actor/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    resource_class = HumorResource
    search_fields = ["title_eng"]
    list_display = ["title_eng","title", "interpreter", "photo", "year", "origen", opciones]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('title_eng',),('title',),('interpreter',),("origen",),('year',),("definition",),
                ),
                "classes": ("games",)
            }
        ), 
        
    )
    class Media:
        css = {
            'all': ('cinema/css/admin.css',)
        }
        js = ("cinema/js/adminhumor.js",)

    def get_queryset(self, request):
        qs = super().get_queryset(request).order_by("title_eng")
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
                
                rank=F("k1") + F("k2"),
                
            ).exclude(rank=0.0).distinct().order_by("-rank", "title_eng")
        else:
            self.ordering = ["title_eng"]
        return qs


class ComboMovieAdminInline(admin.StackedInline):
    model = ComboMovie
    extra = 0


class ComboResource(resources.ModelResource):
    class Meta:
        model = Combo
        exclude = ["id"]
    
@admin.register(Combo)
class ComboModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_actor" data-href-template="/admin/movie/combo/%s/change/" href="/admin/movie/combo/%s/change/" title="Cambiar Combo seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Combo seleccionada/o" href="/admin/movie/combo/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    search_fields = ["name"]
    resource_class = ComboResource
    list_display = ["name", "photo",  opciones]
    inlines = [ComboMovieAdminInline]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('name',),
                ),
                "classes": ("games", "alone")
            }
        ), 
    )
    
    class Media:
        css = {
            'all': ('cinema/css/admin.css',)
        }
        js = ("cinema/js/admin.js",)
    def get_queryset(self, request):
        qs = super().get_queryset(request).order_by("name")
        if "q" in request.GET:
            search_term = request.GET.get("q", "")
            qs = qs.annotate(
                k1=Case(
                    When(name__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(name__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),

                rank=F("k1") + F("k2"),
                
            ).exclude(rank=0.0).distinct().order_by("-rank", "name")
        else:
            self.ordering = ["name"]
        return qs


@admin.register(ComboMovie)
class ComboMovieModelAdmin(admin.ModelAdmin):
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}, models.TextField: {'widget': forms.Textarea(attrs={'cols':38, "style": "margin: 0px 0px 2px; height: 200px; width: 1015px;"})}}


@admin.register(Sagas)
class SagasModelAdmin(admin.ModelAdmin):
    pass
