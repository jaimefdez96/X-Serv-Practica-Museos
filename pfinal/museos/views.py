from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from .models import Museo, Comentario, Conf, Selec
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

#Revisar código
# Help
def lista_distritos(museos):
    lista = list()
    for museo in museos:
        if museo.distrito not in lista:
            lista.append(museo.distrito)
    return(lista)

# Create your views here.
@csrf_exempt
def barra(request):
    metodo = ''
    usuario = ''
    if request.user.is_authenticated():
        usuario = request.user.username
    else:
        usuario = 'login'
    template = get_template('principal.html')
    #Ordenar los museos por comentarios, obtenido de: https://docs.djangoproject.com/en/2.0/topics/db/aggregation/
    #y https://docs.djangoproject.com/en/2.0/ref/models/querysets/
    c = Context({})
    if request.method == 'GET':
        metodo = 'POST'
        museos = Museo.objects.annotate(num_comentarios=Count('comentario')).order_by('-num_comentarios')[:5]
        c = Context({'events' : museos, 'method' : metodo, 'usuario' : usuario})
    elif request.method == 'POST':
        print(request.POST)
        if request.POST['barra'] == 'Accesibles':
            metodo = 'GET'
            museos = Museo.objects.annotate(num_comentarios=Count('comentario')).filter(accesible = True).order_by('-num_comentarios')[:5]
            c = Context({'events' : museos, 'method' : metodo, 'usuario' : usuario})
        else:
            metodo = 'POST'
            ultimo = Museo.objects.all().last().id
            pagina = int(request.POST['barra'])
            first = 0
            last = 0
            if pagina < 5:
                first = 0
                last = 5
            elif pagina + 5 > ultimo:
                first = pagina
                last = ultimo
            else:
                first = pagina + 1
                last = pagina + 5 
            museos = Museo.objects.annotate(num_comentarios=Count('comentario')).order_by('-num_comentarios')[first:last]
            c = Context({'events' : museos, 'method' : metodo, 'usuario' : usuario}) 
    return HttpResponse(template.render(c))
        

@csrf_exempt
def museos(request):
    #https://docs.djangoproject.com/en/2.0/topics/db/queries/
    museos = Museo.objects.all()
    distritos = lista_distritos(museos)
    template = get_template('museos.html')

    if request.method == 'POST':
        distrito = request.POST['distrito']
        print(distrito)
        museos_filtrados = Museo.objects.filter(distrito = distrito)
    else:
        museos_filtrados = Museo.objects.filter(distrito = distritos[0]) #Por defecto, el primer distrito de la lista
    c = Context({'districts' : distritos, 'filt_events' : museos_filtrados})
    return HttpResponse(template.render(c))

def museo(request,num):
    respuesta = ''
    if request.method == 'GET':
        try:
            museo = Museo.objects.get(id=int(num))
            respuesta = museo.nombre + ': ' + museo.descripcion + '<br>'
            respuesta += 'Distrito: ' + museo.distrito + '<br>' + 'Accesible: '
            if museo.accesible:
                respuesta += 'Si<br>'
            else:
                respuesta += 'No<br>'
            respuesta += 'Enlace: esta funcionalidad aun no disponible'
        except Museo.DoesNotExist:
            respuesta = '404 Not Found'

        template = get_template('museo.html')
        c = Context({'event' : respuesta})
        return HttpResponse(template.render(c))
def about(request):
    template = get_template('about.html')
    return HttpResponse(template.render())

def usuario(request,usuario):
    try:
        usuario = User.objects.get(username=usuario)
    except User.DoesNotExist:
        return HttpResponse('<h1>404 Not Found</h1>')
    try:
       museos_de_usuario = Selec.objects.get(usuario=usuario)
    except Selec.DoesNotExist:
        return HttpResponse('<h1>404 Not Found</h1>')#Si el usuario aún no ha escogido ningún museo, debería poner ningún museo escogido
    museos = museos_de_usuario.museo.all()
    if request.user.is_authenticated():
        template = get_template('usuario.html')
        c = Context({'titulo' : 'Página de usuario','events': museos, 'usuario' : request.user.username})
    else:
        None #Debería redirigirlo a login, o a una página login
    return HttpResponse(template.render(c))     
