from django.contrib import admin
from .models import Post, Comentario, VotoComentario, Reaccion


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "autor", "fecha_creacion")
    search_fields = ("titulo", "contenido", "autor__username")
    list_filter = ("fecha_creacion",)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("id", "autor", "post", "contenido_resumido", "fecha_creacion", "destacado", "reportado")
    list_filter = ("destacado", "reportado", "fecha_creacion")
    search_fields = ("contenido", "autor__username", "post__titulo")
    list_editable = ("destacado", "reportado")
    ordering = ("-fecha_creacion",)

    def contenido_resumido(self, obj):
        return (obj.contenido[:50] + "...") if len(obj.contenido) > 50 else obj.contenido
    contenido_resumido.short_description = "Contenido"

    def save_model(self, request, obj, form, change):
        """Si un comentario se marca como destacado, se desmarcan los demás del mismo post."""
        if obj.destacado:
            Comentario.objects.filter(post=obj.post, destacado=True).exclude(id=obj.id).update(destacado=False)
        super().save_model(request, obj, form, change)


@admin.register(VotoComentario)
class VotoComentarioAdmin(admin.ModelAdmin):
    list_display = ("id", "comentario", "usuario", "valor", "fecha")
    list_filter = ("valor", "fecha")
    search_fields = ("comentario__contenido", "usuario__username")


@admin.register(Reaccion)
class ReaccionAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "usuario", "tipo", "fecha")
    list_filter = ("tipo", "fecha")
    search_fields = ("post__titulo", "usuario__username")
