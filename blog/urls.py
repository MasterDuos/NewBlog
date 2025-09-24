from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/<int:id>/", views.post_detalle, name="post_detalle"),  # 👈 nueva ruta
]
