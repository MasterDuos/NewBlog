from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comentario, Reaccion, VotoComentario
from .forms import PostForm, ComentarioForm


# 👉 Página principal
def home(request):
    posts = Post.objects.all().order_by("-fecha_creacion")
    return render(request, "blog/home.html", {"posts": posts})


# 👉 Detalle del post (comentarios + reacciones + votos + destacados)
def post_detalle(request, id):
    post = get_object_or_404(Post, id=id)

    # Formulario de comentario
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

    # 🔹 Separar destacados y normales
    destacados = post.comentarios.filter(destacado=True).order_by("-fecha_creacion")
    normales = sorted(
        post.comentarios.filter(destacado=False),
        key=lambda c: c.votos_totales(),
        reverse=True
    )

    # Conteo de reacciones
    conteos = {
        "like": post.reacciones.filter(tipo="like").count(),
        "love": post.reacciones.filter(tipo="love").count(),
        "laugh": post.reacciones.filter(tipo="laugh").count(),
    }

    # Saber si el usuario ya reaccionó
    ya_reacciono = {"like": False, "love": False, "laugh": False}
    if request.user.is_authenticated:
        ya_reacciono = {
            "like": post.reacciones.filter(usuario=request.user, tipo="like").exists(),
            "love": post.reacciones.filter(usuario=request.user, tipo="love").exists(),
            "laugh": post.reacciones.filter(usuario=request.user, tipo="laugh").exists(),
        }

    return render(request, "blog/post_detalle.html", {
        "post": post,
        "destacados": destacados,   # 👈 sección especial
        "comentarios": normales,    # 👈 resto abajo
        "form": form,
        "conteos": conteos,
        "ya_reacciono": ya_reacciono,
    })


# 👉 Votar comentario (toggle)
@login_required
def votar_comentario(request, comentario_id, valor):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    # Convertimos "up"/"down" a 1/-1
    valor = 1 if valor == "up" else -1

    voto, creado = VotoComentario.objects.get_or_create(
        comentario=comentario,
        usuario=request.user,
        defaults={"valor": valor}
    )

    if not creado:
        if voto.valor == valor:
            voto.delete()
        else:
            voto.valor = valor
            voto.save()

    return redirect("post_detalle", id=comentario.post.id)


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


# 📌 Reportar comentario
@login_required
def reportar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    comentario.reportado = True
    comentario.save()
    return redirect("post_detalle", id=comentario.post.id)


# 📌 Eliminar comentario (solo autor del comentario o admin)
@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user == comentario.autor or request.user.is_superuser:
        comentario.delete()
    return redirect("post_detalle", id=comentario.post.id)


# 📌 Marcar destacado (solo admin)
@login_required
def marcar_destacado(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    if not request.user.is_superuser:
        return redirect("post_detalle", id=comentario.post.id)

    # 🔹 Primero desmarcamos otros comentarios destacados de ese post
    Comentario.objects.filter(post=comentario.post, destacado=True).exclude(id=comentario.id).update(destacado=False)

    # 🔹 Marcamos solo el actual
    comentario.destacado = True
    comentario.save()

    return redirect("post_detalle", id=comentario.post.id)
