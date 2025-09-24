from django.contrib import admin
from .models import Post, Comentario

# 👇 Inline para mostrar comentarios dentro de cada Post
class ComentarioInline(admin.TabularInline):  # también puedes usar StackedInline
    model = Comentario
    extra = 1   # cuántos campos vacíos para añadir comentarios aparecen
    readonly_fields = ("autor", "fecha_creacion")  # estos no se pueden editar desde el inline

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "fecha_creacion")   # columnas visibles
    search_fields = ("titulo", "contenido", "autor__username")  # búsqueda
    list_filter = ("fecha_creacion", "autor")   # filtros laterales
    ordering = ("-fecha_creacion",)   # orden descendente


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("post", "autor", "contenido", "fecha_creacion")
    search_fields = ("contenido", "autor__username", "post__titulo")
    list_filter = ("fecha_creacion", "autor")
    ordering = ("-fecha_creacion",)
