from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="posts/", blank=True, null=True)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    post = models.ForeignKey(Post, related_name="comentarios", on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    reportado = models.BooleanField(default=False)
    destacado = models.BooleanField(default=False)

    def votos_totales(self):
        return self.votos.filter(valor=1).count() - self.votos.filter(valor=-1).count()

    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.post.titulo}"


class VotoComentario(models.Model):
    VALORES = [
        (1, "👍 Voto positivo"),
        (-1, "👎 Voto negativo"),
    ]
    comentario = models.ForeignKey(Comentario, related_name="votos", on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.SmallIntegerField(choices=VALORES)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comentario", "usuario")  # un voto por usuario

    def __str__(self):
        return f"{self.usuario.username} votó {self.valor} en {self.comentario}"


class Reaccion(models.Model):
    REACCIONES_CHOICES = [
        ("like", "👍"),
        ("love", "❤️"),
        ("laugh", "😂"),
    ]
    post = models.ForeignKey(Post, related_name="reacciones", on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=REACCIONES_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "usuario", "tipo")  # evita duplicados exactos

    def __str__(self):
        return f"{self.usuario.username} reaccionó {self.tipo} a {self.post.titulo}"
