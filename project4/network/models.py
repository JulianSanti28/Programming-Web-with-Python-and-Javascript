from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    descripcion = models.CharField(max_length=300, default=None, null = True, blank=True)
    imagen = models.ImageField(upload_to = 'profiles', null = True, blank=True)
    seguidores = models.ManyToManyField('self', related_name='seguidos',related_query_name='seguido', symmetrical=False, blank=True)

class Publicacion(models.Model):

    descripcion = models.CharField(max_length=300, default=None)
    fecha = models.DateTimeField(auto_now_add=True)
    # Relación 1:N con la entidad Usuario
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publicaciones")
    # Representación de cadena

    def __str__(self):
        return f"{self.fecha} By ({self.usuario})"

class Like (models.Model):
    publicacion = models.ForeignKey(
        Publicacion, on_delete=models.CASCADE, related_name="likes")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comentarios")

    def __str__(self):
        return f"{self.publicacion} By ({self.usuario})"
