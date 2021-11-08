from django.contrib import admin

from .models import User, Publicacion, Like

# Register your models here.


class PublicacionSeguimiento(admin.ModelAdmin):
    filter_horizontal = ("Seguidor", "Seguido")


admin.site.register(User)
admin.site.register(Publicacion)
admin.site.register(Like)
