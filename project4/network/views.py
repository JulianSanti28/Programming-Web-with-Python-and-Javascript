from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Publicacion, Like


# Página principal
def index(request):

    LstPublicaciones = []

    publicacionesA = Publicacion.objects.all().order_by('-fecha')

    for i in publicacionesA:

        publicaciones = {}

        likes = Like.objects.filter(publicacion=i).count()

        publicaciones['id'] = i.id
        publicaciones['usuario'] = i.usuario
        publicaciones['descripcion'] = i.descripcion
        publicaciones['fecha'] = i.fecha
        publicaciones['likes'] = likes

        LstPublicaciones.append(publicaciones)

    # Mostrando únicamente 10 publicaciones por página
    paginator = Paginator(LstPublicaciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {"page_obj": page_obj})

# Iniciar sesión


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

# Cerrar sesión


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Registrar usuario


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# Guardar Likes
@csrf_exempt
def add_like(request, publicacion_id):

    # Crear un Like a través del método POST
    if request.method != "PUT":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Capturo los objetos que me importan

    publicacion = Publicacion.objects.get(pk=publicacion_id)
    usuario = User.objects.get(pk=request.user.id)

    # Creando el Like para esa publicacion hecho por el usuario de la sesión
    like = Like(publicacion=publicacion, usuario=usuario)
    like.save()

    likes = Like.objects.filter(publicacion=publicacion).count()

    return JsonResponse({"message": "like add successfully.", "likes": likes}, status=201)


@csrf_exempt
# Remover like
def remove_like(request, publicacion_id):

    # Crear un Like a través del método POST
    if request.method != "PUT":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Capturo los objetos que me importan

    publicacion = Publicacion.objects.get(pk=publicacion_id)
    usuario = User.objects.get(pk=request.user.id)
    # Eliminando el Like
    Like.objects.filter(publicacion=publicacion, usuario=usuario).delete()

    likes = Like.objects.filter(publicacion=publicacion).count()

    return JsonResponse({"message": "like delete successfully.", "likes": likes}, status=201)

# Likes de cada usuario


def likes_user(request):

    LikesU = Like.objects.filter(usuario=request.user.id)
    data = []

    for i in range(len(LikesU)):
        data.append(LikesU[i].publicacion.id)

    return JsonResponse({"LikesU": data}, status=201)


# Ver perfil de un usuario
def view_profile(request, user_id):

    usuario = User.objects.get(pk=user_id)
    LstPublicaciones = []
    publicacionesA = Publicacion.objects.filter(
        usuario=usuario).all().order_by('-fecha')

    for i in publicacionesA:

        publicaciones = {}

        likes = Like.objects.filter(publicacion=i).count()

        publicaciones['id'] = i.id
        publicaciones['usuario'] = i.usuario
        publicaciones['descripcion'] = i.descripcion
        publicaciones['fecha'] = i.fecha
        publicaciones['likes'] = likes

        LstPublicaciones.append(publicaciones)

    # Mostrando únicamente 10 publicaciones por página
    paginator = Paginator(LstPublicaciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    seguidores_count = usuario.seguidores.count()
    seguidos_count = usuario.seguidos.count()

    return render(request, 'network/profile.html', {

        "usuario": usuario, "page_obj": page_obj, "seguidores": seguidores_count, "seguidos": seguidos_count
    })

# Guardar Follow


@csrf_exempt
def add_follow(request, user_id):

    # Crear un Like a través del método POST
    if request.method != "PUT":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Capturo los objetos que me importan

    seguido = User.objects.get(pk=user_id)
    seguidor = User.objects.get(pk=request.user.id)

    seguido.seguidores.add(seguidor)

    seguidores_count = seguido.seguidores.count()
    seguidos_count = seguido.seguidos.count()

    return JsonResponse({"message": "like add successfully.",
                         "seguidores": seguidores_count, "seguidos": seguidos_count}, status=201)

# Remover follow


@csrf_exempt
def remove_follow(request, user_id):

    # Remover Follow a través del método POST
    if request.method != "PUT":
        return JsonResponse({"error": "POST request required."}, status=400)

        # Capturo los objetos que me importan

    seguido = User.objects.get(pk=user_id)
    seguidor = User.objects.get(pk=request.user.id)

    seguido.seguidores.remove(seguidor)

    seguidores_count = seguido.seguidores.count()
    seguidos_count = seguido.seguidos.count()

    return JsonResponse({"message": "like add successfully.",
                         "seguidores": seguidores_count, "seguidos": seguidos_count}, status=201)

# Follows de cada usuario


def follows_user(request):

    usuario = User.objects.get(pk=request.user.id)
    seguidos = usuario.seguidos.all()

    data = []

    for i in range(len(seguidos)):
        data.append(seguidos[i].id)

    return JsonResponse({"SeguidosU": data}, status=201)

# Ver publicaciones d elas personas que sigue


def view_follower(request, user_id):

    # Obteniendo las personas que sigue el usuario.
    Usuario = User.objects.get(pk=user_id)
    seguidos = Usuario.seguidos.all()

    LstPublicaciones = []
    publi_followers = []

    for i in range(0, len(seguidos)):

        publicacionesA = Publicacion.objects.filter(
            usuario=seguidos[i]).all().order_by('-fecha')
        publi_followers.append(publicacionesA)

    for i in range(0, len(publi_followers)):
        for j in range(0, len(publi_followers[i])):

            publicaciones = {}

            likes = Like.objects.filter(
                publicacion=publi_followers[i][j]).count()
            publicaciones['id'] = publi_followers[i][j].id
            publicaciones['usuario'] = publi_followers[i][j].usuario
            publicaciones['descripcion'] = publi_followers[i][j].descripcion
            publicaciones['fecha'] = publi_followers[i][j].fecha
            publicaciones['likes'] = likes
            LstPublicaciones.append(publicaciones)

      # Mostrando únicamente 10 publicaciones por página
    paginator = Paginator(LstPublicaciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/siguiendo.html", {"page_obj": page_obj})

# Agregar un post


def add_post(request):

    if request.method == "POST":
        # Usuario y descripción de la publicacion
        usuario = User.objects.get(pk=request.user.id)
        descripcion = request.POST["descripcion"]
        # Creando y guardando la publicación
        Publi = Publicacion(descripcion=descripcion, usuario=usuario)
        Publi.save()

        return HttpResponseRedirect(reverse("index"))

# Editar un post


@csrf_exempt
def edit_post(request, pub_id):
    
    # Remover Follow a través del método POST
    if request.method != "PUT":
        return JsonResponse({"error": "POST request required."}, status=400)

        # Capturo los objetos que me importan
    # Obteniendo los parámetros enviados por medio del fetch
    data = json.loads(request.body)
    usuario = User.objects.get(pk=request.user.id)
    publicacion = Publicacion.objects.filter(pk=pub_id, usuario=usuario)
    # Actualziando la información de la descripción
    publicacion.update(descripcion=data.get("descripcion"))

    publicacion_actual = Publicacion.objects.get(pk=pub_id, usuario=usuario)

    return JsonResponse({"message": "like add successfully.", "descripcion": publicacion_actual.descripcion}, status=201)
