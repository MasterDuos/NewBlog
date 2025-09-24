from django import forms
from .models import Post, Comentario

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido", "imagen"]  # 👈 incluye imagen
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título del post"}),
            "contenido": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Escribe tu contenido aquí..."}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["contenido"]
        widgets = {
            "contenido": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Escribe un comentario..."
            }),
        }

