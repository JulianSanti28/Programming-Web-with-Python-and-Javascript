from django.shortcuts import render
import markdown2
import random
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse




    
  
def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "val": 1, "tam": len(util.list_entries())
    })


def search(request, search):

    if request.method == "POST":
        search = request.POST.get('q')

        if(util.get_entry(search) == None):

            # Obtener la lista de mis entradas

            list = util.list_entries()
            listAux = []

            for i in range(len(list)):

                if(search.lower() in list[i].lower()):

                    listAux.append(list[i])

            return render(request, "encyclopedia/index.html", {
                "entries": listAux, "val": 2, "tam": len(listAux)
            })
            # Si la entrada existe
        else:

            return render(request, "encyclopedia/entrada.html", {
                "page": markdown2.markdown(util.get_entry(search)), "search": search
            })

    if(util.get_entry(search) == None):
        return render(request, "encyclopedia/entrada.html", {
            "page": None, "search": search
        })
    else:
        return render(request, "encyclopedia/entrada.html", {
            "page": markdown2.markdown(util.get_entry(search)), "search": search
        })


def newPage(request):

    if request.method == "POST":

        title = request.POST.get('titulo')
        content = request.POST.get('contenido')
        # No existe la entrada
        if(util.get_entry(title) == None):
              
            util.save_entry(title, content)

            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(), "val": 1, "tam": len(util.list_entries())
            })
        else:

            return render(request, "encyclopedia/notNewPage.html", {

                "title": title
              })

    else:

        return render(request, "encyclopedia/newPage.html")
      
def editPage(request, title):
      
      
    if request.method == "POST":
    
        title = request.POST.get('titulo')
        content = request.POST.get('contenido')
        util.save_entry(title, content)
        
        return render(request, "encyclopedia/entrada.html", {
            "page": markdown2.markdown(util.get_entry(title)), "search": title
            })
      
      
    else:
      page = util.get_entry(title)
      
      return render(request, "encyclopedia/editPage.html", {
       "content": util.get_entry(title), "title": title
       })
  
    
def randomPage(request):

    # Eligiendo una entrada aleatoria de mi lista de entradas actual
    randomPage = random.choice(util.list_entries())

    return render(request, "encyclopedia/entrada.html", {
        "page": markdown2.markdown(util.get_entry(randomPage)), "search": randomPage
    })
    
