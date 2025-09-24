from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),       # 👈 Home del blog
    path("users/", include("users.urls")),  # 👈 Rutas de usuarios
]

# 👇 Esto agrega soporte a imágenes/media solo si DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
