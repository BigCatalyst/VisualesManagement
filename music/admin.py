from django import forms
from django.db.models import Avg, Case, F, FloatField, Value, When
from django.db.models import Q
from django.db import models
from django.contrib import admin
from music.models import (
    DVD,
    Album,
    AlbumSong,
    Author,
    Collection,
    Concert,
    DVDSong,
    Song,
    Format,
)
from game.admin import AdminImageWidget
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
from django.urls import reverse
from image_helper.widgets import AdminImagePreviewWidget

class EditLinkToInlineObject(object):
    def adicionar_canciones_al_album(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}">{n}</a>'.format(u=url, n=instance.title))
        else:
            return ''

class AlbumResource(resources.ModelResource):
    class Meta:
        model = Album
        exclude = ["id"] 

class AlbumSongAdminInline(admin.StackedInline):
    model = AlbumSong
    extra = 0

@admin.register(Album)
class AlbumModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_movie" data-href-template="/admin/movie/movie/%s/change/" href="/admin/music/album/%s/change/" title="Cambiar Album seleccionado"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Album seleccionada/o" href="/admin/music/album/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    search_fields = ["title"]
    list_display = ["title","author", "photo", "photo_back", "year", opciones]
    inlines = [AlbumSongAdminInline]
    resource_class = AlbumResource
    exclude = ["author_navigation_id"]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('title',),("year",),('photo_back',),('author',)
                ),
                "classes": ("games","alone2", "name")
            }
        ), 
    )
    
    class Media:
        css = {
            'all': ('cinema/css/dvd.css',)
        }
        js = ("cinema/js/admin.js",)

    def get_queryset(self, request):
        qs = super().get_queryset(request).order_by("title")
        if "q" in request.GET:
            search_term = request.GET.get("q", "")
            qs = qs.annotate(
                k1=Case(
                    When(title__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(title__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k3=Case(
                    When(author__name__istartswith=search_term, then=Value(1)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k4=Case(
                    When(author__name__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                
                rank=F("k1") + F("k2"),
                rank2=F("k3") + F("k4"),
                
            ).exclude(rank=0.0).distinct().order_by("-rank", "-rank2", "title")
        else:
            self.ordering = ["title"]
        return qs
        
class AlbumAdminInline(EditLinkToInlineObject,admin.StackedInline):
    model = Album
    readonly_fields = ('adicionar_canciones_al_album', )
    exclude = ["author_navigation_id"]
    extra = 0
    formfield_overrides = {models.ImageField: {'widget': AdminImagePreviewWidget}}
    

    
class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author
        exclude = ["id"] 


@admin.register(Author)
class AuthorModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_movie" data-href-template="/admin/movie/movie/%s/change/" href="/admin/music/author/%s/change/" title="Cambiar Película seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Pelicula seleccionada/o" href="/admin/music/author/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    
    def albums(obj):
        return mark_safe("<br/>".join([album.title for album in Album.objects.filter(author_id=obj.id)]))
    albums.short_description = "Albums"
    albums.allow_tags = True
    albums.admin_order_field = 'album__title'
    inlines = [AlbumAdminInline]
    resource_class = AuthorResource
    search_fields = ["name"]
    list_display = ["name", "photo", albums, opciones]
    
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
            'all': ('cinema/css/author.css',)
        }
        js = ("cinema/js/adminauthor.js",)

    def get_queryset(self, request):
        q = super().get_queryset(request)
        return q.exclude(album=None)

class ConcertResource(resources.ModelResource):
    class Meta:
        model = Concert
        exclude = ["id"] 

@admin.register(Concert)
class ConcertModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_movie" data-href-template="/admin/movie/movie/%s/change/" href="/admin/music/concert/%s/change/" title="Cambiar Película seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Pelicula seleccionada/o" href="/admin/music/concert/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    resource_class = ConcertResource
    search_fields = ["interpreter"]
    list_display = ["interpreter","place", "year", "definition", "photo", opciones]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('interpreter',),("place",),('year',),("definition",),
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
        qs = super().get_queryset(request).order_by("interpreter")
        if "q" in request.GET:
            search_term = request.GET.get("q", "")
            qs = qs.annotate(
                k1=Case(
                    When(interpreter__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(interpreter__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                
                rank=F("k1") + F("k2"),
                
            ).exclude(rank=0.0).distinct().order_by("-rank", "interpreter")
        else:
            self.ordering = ["interpreter"]
        return qs

@admin.register(AlbumSong)
class AlbumSongModelAdmin(admin.ModelAdmin):
    pass

    
class DVDSongAdminInline(admin.StackedInline):
    model = DVDSong
    extra = 0

class DVDResource(resources.ModelResource):
    class Meta:
        model = DVD
        exclude = ["id"] 


@admin.register(DVD)
class DVDModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_movie" data-href-template="/admin/movie/movie/%s/change/" href="/admin/music/dvd/%s/change/" title="Cambiar Película seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Pelicula seleccionada/o" href="/admin/music/dvd/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    search_fields = ["title", "author__name"]
    resource_class = DVDResource
    list_display = ["title","author", "year", "photo", "photo_back", opciones]
    inlines = [DVDSongAdminInline]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('title',),("year",),('author',),('photo_back',),
                ),
                "classes": ("games","alone2", "name")
            }
        ), 
    )
    
    class Media:
        css = {
            'all': ('cinema/css/dvd.css',)
        }
        js = ("cinema/js/admin.js",)

    def get_queryset(self, request):
        qs = super().get_queryset(request).order_by("title")
        if "q" in request.GET:
            search_term = request.GET.get("q", "")
            qs = qs.annotate(
                k1=Case(
                    When(title__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(title__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k3=Case(
                    When(author__name__istartswith=search_term, then=Value(1)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k4=Case(
                    When(author__name__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                
                rank=F("k1") + F("k2"),
                rank2=F("k3") + F("k4")
            ).exclude(rank=0.0, rank2=0.0).distinct().order_by("-rank", "-rank2", "title")
        else:
            self.ordering = ["title"]
        return qs

@admin.register(DVDSong)
class DVDSongModelAdmin(admin.ModelAdmin):
    pass


class SongAdminInline(admin.StackedInline):
    model = Song
    extra = 0

class CollectionResource(resources.ModelResource):
    class Meta:
        model = Collection
        exclude = ["id"] 

    
@admin.register(Collection)
class CollectionModelAdmin(ImportExportModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(CollectionModelAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['format'].initial = Format.objects.get(id=21)
        return form
    def opciones(obj):
        return mark_safe(u'<a id="change_id_movie" data-href-template="/admin/movie/movie/%s/change/" href="/admin/music/collection/%s/change/" title="Cambiar Película seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Pelicula seleccionada/o" href="/admin/music/collection/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    
    search_fields = ["name", "gender__name"]
    resource_class = CollectionResource
    list_display = ["name","gender", "photo", opciones]
    inlines = [SongAdminInline]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('name',),("gender",), ("format",)
                ),
                "classes": ("games", "alone name")
            }
        ), 
    )
    
    class Media:
        css = {
            'all': ('cinema/css/collection.css',)
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
                k3=Case(
                    When(gender__name__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k4=Case(
                    When(gender__name__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                rank=F("k1") + F("k2"),
                rank2=F("k3") + F("k4"),
                
            ).exclude(rank=0.0, rank2=0.0).distinct().order_by("-rank", "-rank2", "name")
        else:
            self.ordering = ["name"]
        return qs


@admin.register(Song)
class SongModelAdmin(admin.ModelAdmin):
    pass
