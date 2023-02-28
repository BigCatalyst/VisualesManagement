from django import forms
from django.db.models import Avg, Case, F, FloatField, Value, When
from django.db.models import Q
from django.db import models
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from game.models import Category, Game, GameCapture
from django.utils.safestring import mark_safe
from image_helper.widgets import AdminImagePreviewWidget



class GameResource(resources.ModelResource):
    class Meta:
        model = Game
        exclude = ["id"] 
        
    @staticmethod
    def dehydrate_category(instance):   
        return '%s' % instance.category.name


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        img_id = "form_photo" if name == "photo" else "form_photo_back"
        
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
        else:
            image_url = "/static/cinema/images/benito2.svg"
        file_name = str(value)
        output.append(u' <img src="%s" id="%s" alt="%s"  style="object-fit: fill; width: 248px; height: 230px;"/> ' %(image_url,img_id, file_name))
        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))


class AdminVideoWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
        else:
            image_url = "/static/cinema/images/video.svg"
        file_name = str(value)
        output.append(u' <img src="%s" id="form_video" alt="%s"  style="object-fit: fill; width: 248px; height: 230px;"/> ' %(image_url, file_name))
        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))

class GameCaptureAdminInline(admin.StackedInline):
    model = GameCapture
    extra = 0
    max_num = 3
    formfield_overrides = {
        models.ImageField: {'widget': AdminImagePreviewWidget}, 
    }


@admin.register(Game)
class GameModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_actor" data-href-template="/admin/movie/combo/%s/change/" href="/admin/game/game/%s/change/" title="Cambiar Juego seleccionado"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Juego seleccionado" href="/admin/game/game/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    search_fields = ["name", "category__name"]
    list_display = ["name", "category", "year", "photo", "synopsis", "size",  opciones]
    inlines = [GameCaptureAdminInline,]
    resource_class = GameResource
    exclude = ["rawg", "reviewed"]
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}, 
        models.TextField: {'widget': forms.Textarea(attrs={'cols':23, "style": "margin: 0px 0px 2px; height: 211px; width: 292px;"})},
        models.FileField: {'widget': AdminVideoWidget}
    }

    class Media:
        css = {
            'all': ('cinema/css/game.css',)
        }
        js = ("cinema/js/admin.js",)
        
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',),('name',), ('category',),("year",), ("type",), ("size",),('manual',),('requirement',), ('synopsis',),
                ),
                "classes": ("games",)
            }
        ), 
    )
    
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
                    When(category__name__istartswith=search_term, then=Value(1)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k4=Case(
                    When(category__name__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                
                rank=F("k1") + F("k2"),
                rank2=F("k3") + F("k4"),
                
            ).exclude(rank=0.0, rank2=0.0).distinct().order_by("-rank", "-rank2", "name")
        else:
            self.ordering = ["name"]
        return qs

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        exclude = ["id"]     

@admin.register(Category)
class CategoryModelAdmin(ImportExportModelAdmin):
    def opciones(obj):
        return mark_safe(u'<a id="change_id_actor" data-href-template="/admin/movie/combo/%s/change/" href="/admin/game/category/%s/change/" title="Cambiar Categoría seleccionada"><img src="/static/images/edit.png" alt="Modificar"></a><a class="related-widget-wrapper-link delete-related" id="delete_id_format" data-href-template="/admin/movie/format/{}/delete/?_to_field=format&amp;_popup=1" title="Eliminar Categoría seleccionada" href="/admin/game/category/%s/delete/"><img src="/static/images/delete.png" alt="Eliminar"></a>' % (obj.id, obj.id, obj.id))
       
    opciones.short_description = "Acciones"
    opciones.allow_tags = True
    list_display = ["name", "photo", "photo_back",  opciones]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    resource_class = CategoryResource
    fieldsets=(        
        ("",{
                "fields": ( 
                    ('photo',), ('name',), ('photo_back',),
                ),
                "classes": ("games", "alone",)
            }
        ), 
    )
    
    class Media:
        css = {
            'all': ('cinema/css/dvd.css',)
        }
        js = ("cinema/js/admin.js",)
        


@admin.register(GameCapture)
class GameCaptureModelAdmin(admin.ModelAdmin):
    pass
