from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms



CATEGORIAS_CHOICES = (
    ('Tecnology','Tecnology'),
    ('Fashion', 'Fashion'),
    ('Beauty','Beauty'),
    ('Home','Home')
    
)


class User(AbstractUser):
    pass
  
    
    
class Usuario(models.Model):
    
    nombre_usuario = models.CharField(max_length=300, blank=False)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=300, blank=False)
    
    def __str__(self):
        return f"{self.nombre_usuario}"
    




class Oferta(models.Model):
    
    precio = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="ofertas")
    #Representación de cadena para cualquier aeropuesto que se encuentre en esta tabla
    def __str__(self):
        return f"{self.precio} By ({self.usuario})"
    
    

    
class Comentario(models.Model):
    
    descripcion = models.CharField(max_length=300, default=None)
    fecha = models.DateTimeField(auto_now_add = True)
    #Relación 1:N con la entidad Usuario
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="comentarios")
    #Representación de cadena para cualquier aeropuesto que se encuentre en esta tabla
    def __str__(self):
        return f"{self.fecha} By ({self.usuario})"
    
    


class Subasta(models.Model):
    
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_CHOICES, default='Hogar')
    precioInicial = models.IntegerField()
    imagen = models.ImageField(upload_to = 'subastas', null= True)
    #Rleacion 1:N entre la entidad usuario y la entidad Subasta
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="subastasU")
    #Relacion N:M Entre la entidad Subasta con las entidades Oferta, Comentario
    comentarios = models.ManyToManyField(Comentario, blank=True, related_name="subastasC")
    ofertas = models.ManyToManyField(Oferta, blank=True, related_name="subastasO")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        
        return f"{self.titulo} By: ({self.usuario}) \n  Description: {self.descripcion} \n Precio: {self.precioInicial} "
    
    
class Seguimiento(models.Model):
        
     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
     subasta= models.ForeignKey(Subasta, on_delete=models.CASCADE)
     
     
     def __str__(self):
            
        return f"{self.subasta} "
    
class Ganada(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null= False, blank=False)
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE, null= False, blank=False)
    
    def __str__(self):
            
        return f"{self.usuario} Won: ({self.subasta}) "
    
    
    

    
