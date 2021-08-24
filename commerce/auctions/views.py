from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Subasta, Oferta, Comentario, Usuario, Ganada, Seguimiento
from django import forms

from django.contrib.auth.decorators import login_required

# add for me
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORIAS_CHOICES = (
    ('Tecnology', 'Tecnology'),
    ('Fashion', 'Fashion'),
    ('Beauty', 'Beauty'),
    ('Home', 'Home')

)


class NewSubastaForm(forms.Form):
    titulo = forms.CharField(label='Title:', max_length=100)
    descripcion = forms.CharField(label='Description:', max_length=100)
    categoria = forms.ChoiceField(label='Category', choices=CATEGORIAS_CHOICES)
    precio_inicial = forms.IntegerField(label='$')

   


def index(request):
    
    
    subastas = Subasta.objects.exclude(estado=False).all()
    
    subastasRe = subastas.order_by('precioInicial')
    
    
    return render(request, "auctions/index.html", {
        # Obteniendo todos los objetos instanciado de mi clase Subasta
        "subastas": subastasRe

    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:

        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user1 = Usuario(nombre_usuario=username,
                            email=email, password=password)
            user.save()
            user1.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

    # add for me

def subasta(request, sub_id):

    # Obtener la subasta con el id correspondiente
    subasta = Subasta.objects.get(pk=sub_id)
    comentarios = subasta.comentarios.all()
    aux = subasta.usuario.id

    # Mejor oferta actual
    ofertas = subasta.ofertas.all()
    Mayor = 0

    if len(ofertas) > 0:

        Mayor = 0

        for i in range(len(ofertas)):
            oferta = ofertas[i].precio
            if oferta > Mayor:
                Mayor = ofertas[i].precio
                mejorOferta = ofertas[i]

    return render(request, "auctions/subasta.html", {

        "sub": subasta, "comentarios": comentarios, "usuario": aux+1, "mejorOferta": Mayor

    })

@login_required
def agregar_comentario(request, sub_id, user_id):

    # Crear el comentario

    if request.method == "POST":

        # Capturo los objetos que me importan
        subasta = Subasta.objects.get(pk=sub_id)
        usuario = Usuario.objects.get(pk=user_id-1)
        # Capturo la descripción del comentario
        descripcion = request.POST["descripcion"]

        # Creando el comentario por ese usuario en específico
        comentario = Comentario(descripcion=descripcion, usuario=usuario)
        comentario.save()
        # Agregando el comentarioa la subasta específica
        subasta.comentarios.add(comentario)
        # Comentarios de la subasta
        comentarios = subasta.comentarios.all()

        return HttpResponseRedirect(reverse("subasta", kwargs={"sub_id": sub_id}))

@login_required
def agregar_subasta(request, user_id):
    
    

    if request.method == "POST":
        
        

        form = NewSubastaForm(request.POST)

        if form.is_valid():

            titulo = form.cleaned_data["titulo"]
            descripcion = form.cleaned_data["descripcion"]
            categoria = form.cleaned_data["categoria"]
            imagen = request.FILES.get("imagenSub")
            precio_inicial = int(form.cleaned_data["precio_inicial"])

            # Capturar el usuario
            usuario = Usuario.objects.get(pk=user_id-1)

            subasta = Subasta(titulo=titulo, descripcion=descripcion, categoria=categoria, precioInicial=precio_inicial,
                              imagen=imagen, usuario=usuario)

            subasta.save()

            return HttpResponseRedirect(reverse("index"))

    form = NewSubastaForm()

    return render(request, "auctions/add_subasta.html", {
        "form": form

    })

@login_required
def agregar_oferta(request, sub_id, user_id):

    bandera = True

    if request.method == "POST":

        subasta = Subasta.objects.get(pk=sub_id)
        precio_inicial = subasta.precioInicial
        precioDigitado = int(request.POST["offer"])

        if (precioDigitado > precio_inicial):

            # Ontengo todas las ofertas de esta subasta
            ofertas = subasta.ofertas.all()

            for i in range(len(ofertas)):

                if (int(request.POST["offer"]) > ofertas[i].precio):

                    bandera = True
                else:

                    bandera = False

            if bandera:

                # Capturo los objetos que me importan
                usuario = Usuario.objects.get(pk=user_id-1)
                # Capturo la descripción del valor de la oferta
                valor = request.POST["offer"]
                oferta = Oferta(precio=int(valor), usuario=usuario)
                oferta.save()
                # Agregando el comentarioa la subasta específica
                subasta.ofertas.add(oferta)

                # Mejor oferta actual
                ofertas = subasta.ofertas.all()
                Mayor = 0

                if len(ofertas) > 0:

                    for i in range(len(ofertas)):
                        oferta = ofertas[i].precio
                        if oferta > Mayor:
                            Mayor = ofertas[i].precio
                            mejorOferta = ofertas[i]

                aux = user_id

                return render(request, "auctions/subasta.html", {

                    "sub": subasta, "comentarios": subasta.comentarios.all(), "usuario": aux+1, "confirmacion": "Congratulations! Offer added!", "mejorOferta": Mayor

                })
            else:

                # Mejor oferta actual
                ofertas = subasta.ofertas.all()
                Mayor = 0

                if len(ofertas) > 0:

                    for i in range(len(ofertas)):
                        oferta = ofertas[i].precio
                        if oferta > Mayor:
                            Mayor = ofertas[i].precio
                            mejorOferta = ofertas[i]

                aux = user_id

                return render(request, "auctions/subasta.html", {

                    "sub": subasta, "comentarios": subasta.comentarios.all(), "usuario": aux+1, "error": "¡Ups! There are better deals", "mejorOferta": Mayor

                })

        else:

            # Mejor oferta actual
            ofertas = subasta.ofertas.all()
            Mayor = 0

            if len(ofertas) > 0:

                for i in range(len(ofertas)):
                    oferta = ofertas[i].precio
                    if oferta > Mayor:
                        Mayor = ofertas[i].precio
                        mejorOferta = ofertas[i]

            aux = user_id

            return render(request, "auctions/subasta.html", {

                "sub": subasta, "comentarios": subasta.comentarios.all(), "usuario": aux+1, "error": "¡Ups! You do not exceed the initial offer", "mejorOferta": Mayor

            })

@login_required
def cerrar_subasta(request, sub_id):

    mejorOferta = None

    if request.method == "POST":
        # Obteniendo el objeto de la subasta en cuestión
        subasta = Subasta.objects.get(pk=sub_id)
        # Ofertas de esas ofertas
        ofertas = subasta.ofertas.all()

        if len(ofertas) > 0:

            Mayor = 0

            for i in range(len(ofertas)):

                print(ofertas[i])

                oferta = ofertas[i].precio

                if oferta > Mayor:
                    Mayor = ofertas[i].precio
                    mejorOferta = ofertas[i]

            usuarioM = mejorOferta.usuario

            ofertaG = Ganada(usuario=usuarioM, subasta=subasta)
            ofertaG.save()
            subasta.estado = False
            subasta.save()

            return HttpResponseRedirect(reverse("index"))

        else:
            subasta.estado = False
            subasta.save()

            return HttpResponseRedirect(reverse("index"))

@login_required
def notificacion(request, user_id):

    usuario = Usuario.objects.get(pk=user_id-1)

    ganadas = Ganada.objects.filter(usuario=usuario).all()

    return render(request, "auctions/notificaciones.html", {"notificaciones": ganadas})

@login_required
def seguimiento(request, sub_id, user_id):

    

    bandera = False

    if request.method == "POST":

        subasta = Subasta.objects.get(pk=sub_id)
        usuario = Usuario.objects.get(pk=user_id-1)

        seguimientos = Seguimiento.objects.filter(usuario=usuario, subasta=subasta).count()

        if seguimientos > 0:

            aux = user_id
            return render(request, "auctions/subasta.html", {

                "sub": subasta, "comentarios": subasta.comentarios.all(), "usuario": aux+1, "error": "This auction already exists in your watchlist", "mejorOferta": 0

            })

        else:

            try:
                
                
                
                newSeguimiento = Seguimiento(usuario=usuario, subasta=subasta)
                newSeguimiento.save()
                #Cantidad de seguimientos del usuario
                seguimientos = Seguimiento.objects.filter(usuario=usuario).count()
                
                # Mejor oferta actual
                ofertas = subasta.ofertas.all()
                Mayor = 0

                if len(ofertas) > 0:

                  for i in range(len(ofertas)):
                     oferta = ofertas[i].precio
                     if oferta > Mayor:
                        Mayor = ofertas[i].precio
                        mejorOferta = ofertas[i]

                aux = user_id
                return render(request, "auctions/subasta.html", {

                    "sub": subasta, "comentarios": subasta.comentarios.all(), "usuario": aux+1, "confirmacion": "Successfully added!", "mejorOferta": Mayor, "cont":seguimientos
                    

                })

            except:

                aux = user_id

                return render(request, "auctions/subasta.html", {

                    "sub": subasta, "comentarios": subasta.comentarios.all(), "usuario": aux+1, "error": "Not added correctly", "mejorOferta": 0

                })

    else:
        #Cantidad de seguimientos del usuario
        usuario = Usuario.objects.get(pk=user_id-1)
        Cseguimientos = Seguimiento.objects.filter(usuario=usuario).count()
        usuario = Usuario.objects.get(pk=user_id-1)
        seguimientos = Seguimiento.objects.filter(usuario=usuario).all()

        return render(request, "auctions/seguimiento.html", {
            
            

            "seguimientos": seguimientos, "cont":Cseguimientos

        })

@login_required
def remover_seguimiento(request, sub_id, user_id):

    if request.method == "POST":

        usuario = Usuario.objects.get(pk=user_id-1)
        subasta = Subasta.objects.get(pk=sub_id)

        Seguimiento.objects.filter(usuario=usuario, subasta=subasta).delete()

        usuario = Usuario.objects.get(pk=user_id-1)
        seguimientos = Seguimiento.objects.filter(usuario=usuario).all()

        # return render(request, "auctions/seguimiento.html", {

        #   "seguimientos": seguimientos

        # })

        return HttpResponseRedirect(reverse("seguimiento", kwargs={"sub_id": sub_id, "user_id": user_id}))
     #   return HttpResponseRedirect("Congratulations!")

    #return HttpResponde("Congratulations!")
    
@login_required
def categorias(request):
    
     categorias = set()
     subastas = Subasta.objects.all()
     
     for i in range(len(subastas)):
         
         categorias.add(subastas[i].categoria)
         
     return render(request, 'auctions/categorias.html', {
        
        "categorias": categorias
    })
@login_required
def categoria(request, categoria):
    
    subastas = Subasta.objects.exclude(estado=False).all()
    subastasCat = subastas.filter(categoria=categoria).all()

    
    
    return render(request, "auctions/index.html", {
        # Obteniendo todos los objetos instanciado de mi clase Subasta
        "subastas": subastasCat

    })
    
         
        
        
        
        

