from django.urls import path
from django.conf import settings
from django.conf.urls.static import static





from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("register", views.register, name="register"),
    path("<int:sub_id>/details", views.subasta, name="subasta"),
    path("<int:sub_id>/<int:user_id>/addcomment", views.agregar_comentario, name="agregarC"),
    path("<int:user_id>/addAuction", views.agregar_subasta, name="agregarS"),
    path("<int:sub_id>/<int:user_id>/addoffer", views.agregar_oferta, name="agregarO"),
    path("<int:sub_id>/close", views.cerrar_subasta, name="cerrarS"),
    path("<int:user_id>/notifications", views.notificacion, name="notificar"),
    path("<int:sub_id>/<int:user_id>/whatchList", views.seguimiento, name="seguimiento"),
    path("<int:sub_id>/<int:user_id>/remove", views.remover_seguimiento, name="remover"),
    path("categories", views.categorias, name="categorias"),
    path("categories/<str:categoria>", views.categoria, name="categoria")
    
] 

 






