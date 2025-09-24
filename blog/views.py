from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all().order_by('-fecha_creacion')
    return render(request, "blog/home.html", {"posts": posts})

from django.shortcuts import render, get_object_or_404

def post_detalle(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, "blog/post_detalle.html", {"post": post})
