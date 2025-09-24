from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comentario, Reaccion
from .forms import PostForm, ComentarioForm


# 📌 Página principal: lista de posts
def home(request):
    posts = Post.objects.all().order_by('-fecha_creacion')
    return render(request, "blog/home.html", {"posts": posts})


# 📌 Detalle de un post (comentarios + reacciones)
def post_detalle(request, id):
    post = get_object_or_404(Post, id=id)
    comentarios = post.comentarios.all().order_by("-fecha_creacion")

    # 👉 Manejo de comentarios
    if request.method == "POST" and "comentario" in request.POST:
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.post = post
                comentario.autor = request.user
                comentario.save()
                return redirect("post_detalle", id=post.id)
        else:
            return redirect("login")
    else:
        form = ComentarioForm()

    # 👉 Conteo de reacciones
    conteos = {
        "like": post.reacciones.filter(tipo="like").count(),
        "love": post.reacciones.filter(tipo="love").count(),
        "laugh": post.reacciones.filter(tipo="laugh").count(),
    }

    # 👉 Saber si el usuario ya reaccionó
    ya_reacciono = {
        "like": False,
        "love": False,
        "laugh": False,
    }
    if request.user.is_authenticated:
        ya_reacciono = {
            "like": post.reacciones.filter(usuario=request.user, tipo="like").exists(),
            "love": post.reacciones.filter(usuario=request.user, tipo="love").exists(),
            "laugh": post.reacciones.filter(usuario=request.user, tipo="laugh").exists(),
        }

    return render(request, "blog/post_detalle.html", {
        "post": post,
        "comentarios": comentarios,
        "form": form,
        "conteos": conteos,
        "ya_reacciono": ya_reacciono,
    })


# 📌 Crear post (solo logueados)
@login_required
def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "blog/crear_post.html", {"form": form})


# 📌 Editar post (solo autor)
@login_required
def editar_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.autor != request.user:
        return redirect("home")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detalle", id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/editar_post.html", {"form": form, "post": post})


# 📌 Eliminar post (solo autor)
@login_required
def eliminar_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.autor != request.user:
        return redirect("home")
    if request.method == "POST":
        post.delete()
        return redirect("home")
    return render(request, "blog/eliminar_post.html", {"post": post})


# 📌 Reaccionar (toggle)
@login_required
def reaccionar(request, id, tipo):
    post = get_object_or_404(Post, id=id)
    reaccion, creada = Reaccion.objects.get_or_create(post=post, usuario=request.user, tipo=tipo)
    if not creada:  # si ya existía, la quitamos (toggle)
        reaccion.delete()
    return redirect("post_detalle", id=post.id)
