
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("likes/<int:publicacion_id>", views.add_like, name="add_likes"),
    path("likes/delete/<int:publicacion_id>",views.remove_like, name="remove_likes"),
    path("likes-user", views.likes_user, name="user_likes"),
    path("profile/<int:user_id>", views.view_profile, name="view_profile"),
    path("follow/<int:user_id>", views.add_follow, name="add_follow"),
    path("remove/follow/<int:user_id>",views.remove_follow, name="remove_follow"),
    path("follows-user", views.follows_user, name="follows_likes"),
    path("view_follower/<int:user_id>", views.view_follower, name="view_follower"),
    path("add_post", views.add_post, name="add_post"),
    path("edit_post/<int:pub_id>", views.edit_post, name="edit_post"),
 

    




]
