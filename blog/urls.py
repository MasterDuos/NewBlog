from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/<int:id>/", views.post_detalle, name="post_detalle"),
    path("crear/", views.crear_post, name="crear_post"),
    path("editar/<int:id>/", views.editar_post, name="editar_post"),
    path("eliminar/<int:id>/", views.eliminar_post, name="eliminar_post"),
    path("post/<int:id>/reaccion/<str:tipo>/", views.reaccionar, name="reaccionar"),
]
