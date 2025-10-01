from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Página principal
    path("", views.home, name="home"),

    # 📌 Posts
    path("post/<int:id>/", views.post_detalle, name="post_detalle"),
    path("crear/", views.crear_post, name="crear_post"),
    path("post/<int:id>/editar/", views.editar_post, name="editar_post"),
    path("post/<int:id>/eliminar/", views.eliminar_post, name="eliminar_post"),

    # 📌 Reacciones en posts
    path("post/<int:id>/reaccionar/<str:tipo>/", views.reaccionar, name="reaccionar"),

    # 📌 Votos en comentarios
    path("comentario/<int:comentario_id>/votar/<str:valor>/", views.votar_comentario, name="votar_comentario"),
    
    # 📌 Reportar comentario 
    path("comentario/<int:comentario_id>/reportar/", views.reportar_comentario, name="reportar_comentario"),
    path("comentario/<int:comentario_id>/eliminar/", views.eliminar_comentario, name="eliminar_comentario"),

    # 📌 Destacado
    path("comentario/<int:comentario_id>/destacar/", views.marcar_destacado, name="marcar_destacado"),

    path("notificaciones/", views.notificaciones, name="notificaciones"),
    path("notificaciones/<int:id>/leida/", views.marcar_leida, name="marcar_leida"),
    path("comentario/<int:comentario_id>/votar/<str:valor>/", views.votar_comentario, name="votar_comentario"),  # 'up'/'down'

]
