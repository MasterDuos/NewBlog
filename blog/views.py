from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all().order_by('-fecha_creacion')
    return render(request, "blog/home.html", {"posts": posts})

from django.shortcuts import render, get_object_or_404

def post_detalle(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, "blog/post_detalle.html", {"post": post})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PostForm

@login_required
def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "blog/crear_post.html", {"form": form})
