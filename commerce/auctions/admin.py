

from django.contrib import admin

from .models import Oferta, Subasta, Comentario, Usuario, Seguimiento, Ganada

# Register your models here.


class SubastaAdmin(admin.ModelAdmin):
    filter_horizontal = ("comentarios", "ofertas")


admin.site.register(Oferta)
admin.site.register(Subasta, SubastaAdmin)
admin.site.register(Comentario)
admin.site.register(Usuario)
admin.site.register(Seguimiento)
admin.site.register(Ganada)

