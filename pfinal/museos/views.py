from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from .models import Museo, Comentario, Conf, Selec
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
#from django.contrib.auth import authenticate, login
#from django.contrib.auth import logout
from django.utils import timezone

#Revisar código
# Help
def lista_distritos(museos):
    lista = list()
    for museo in museos:
        if museo.distrito not in lista:
            lista.append(museo.distrito)
    return(lista)

def filtrar_museos(accesibles,first,last):
    if accesibles == True:
        museos = Museo.objects.annotate(num_comentarios=Count('comentario')).filter(accesible = True).order_by('-num_comentarios')[first:last]
    else:
        museos = Museo.objects.annotate(num_comentarios=Count('comentario')).order_by('-num_comentarios')[first:last]
    return museos

#Revisar esta funcion
def paginas(pagina,ultimo):
    first = 0
    last = 0
    if pagina < 5:
        first = 0
        if ultimo < 5:
            last = ultimo
        else:
            last = 5
    elif pagina + 5 > ultimo:
        first = pagina
        last = ultimo
    else:
        first = pagina + 1
        last = pagina + 5
    return(first,last) 

# Create your views here.

# Login/Logout: https://docs.djangoproject.com/en/2.0/topics/auth/default/

#El barra funciona bien pero hay que revisarlo
@csrf_exempt
def barra(request):
    usuario = ''
    metodo = ''
    usuarios = User.objects.all()
    #Esto debería ser una funcion, aunque es provisional
    if request.user.is_authenticated():
        usuario = request.user.username
    else:
        usuario = 'login'
    template = get_template('principal.html')
    #Ordenar los museos por comentarios, obtenido de: https://docs.djangoproject.com/en/2.0/topics/db/aggregation/
    #y https://docs.djangoproject.com/en/2.0/ref/models/querysets/
    c = Context({})
    if request.method == 'GET':
        accesibles = False  
        metodo = 'POST'
        #if request.GET['barra'] == 'Accesibles':
        museos = filtrar_museos(accesibles,0,5)#Siempre que pido la página principal, me devuelve los 5 más comentados
        c = Context({'events' : museos, 'method' : metodo, 'usuario' : usuario, 'check': accesibles, 'users' : usuarios})
    elif request.method == 'POST':
        print(request.POST)#Traza
        if request.POST['barra'] == 'Accesibles':
            metodo = 'GET'
            accesibles = True
            museos = filtrar_museos(accesibles,0,5)
        else:
            num_museos = 0
            accesibles = request.POST['accesible']
            if accesibles == 'False': #OJO, es un string, no un boolean
                num_museos = Museo.objects.all().count()
                accesibles = False
                metodo = 'POST'
            else:
                num_museos = Museo.objects.filter(accesible = True).count()
                accesibles = True
                metodo = 'GET'

            pagina = int(request.POST['barra'])
            first,last = paginas(pagina,num_museos)
            museos = filtrar_museos(accesibles,first,last)
        c = Context({'events' : museos, 'method':metodo, 'usuario' : usuario, 'check' : accesibles, 'users' : usuarios}) 
    return HttpResponse(template.render(c))
        

@csrf_exempt
def museos(request):
    #https://docs.djangoproject.com/en/2.0/topics/db/queries/
    #Esto debería ser una funcion, aunque es provisional
    if request.user.is_authenticated():
        usuario = request.user.username
    else:
        usuario = 'login'
    museos = Museo.objects.all()
    distritos = lista_distritos(museos)
    template = get_template('museos.html')

    if request.method == 'POST':
        distrito = request.POST['distrito']
        print(distrito)
        museos_filtrados = Museo.objects.filter(distrito = distrito)
    else:
        museos_filtrados = Museo.objects.filter(distrito = distritos[0]) #Por defecto, el primer distrito de la lista
    c = Context({'districts' : distritos, 'filt_events' : museos_filtrados,'usuario' : usuario})
    return HttpResponse(template.render(c))

@csrf_exempt
def museo(request,num):
    respuesta = ''
    #Esto debería ser una funcion, aunque es provisional
    if request.user.is_authenticated():
        usuario = request.user.username
    else:
        usuario = 'login'

    try: 
        museo = Museo.objects.get(id=int(num))
        if request.method == 'GET':
            respuesta = museo.nombre + ': ' + museo.descripcion + '<br>'
            respuesta += 'Distrito: ' + museo.distrito + '<br>' + 'Accesible: '
            if museo.accesible:
                respuesta += 'Si<br>'
            else:
                respuesta += 'No<br>'
            respuesta += 'Enlace: esta funcionalidad aun no disponible'
        elif request.method == 'POST':
            print(request.POST)
            if request.POST['museo']=='Like':
                try:
                    museos_de_usuario = Selec.objects.get(usuario=request.user)
                    if museo not in museos_de_usuario.museo.all():
                        museos_de_usuario.museo.add(museo)
                except Selec.DoesNotExist:
                    nuevo_selec = Selec(usuario = request.user, museo = museo, fecha = timezone.now())
                    nuevo_selec.save()
                return HttpResponseRedirect('/museo/'+num)
            else:
                comentario = Comentario(autor = request.POST['usuario'], texto = request.POST['museo'], museo = museo, fecha =
timezone.now())
                comentario.save()
                return HttpResponseRedirect('/')    
    except Museo.DoesNotExist:
            respuesta = '404 Not Found'

    template = get_template('museo.html')
    c = Context({'user' : request.user,'event' : respuesta, 'usuario' : usuario})
    return HttpResponse(template.render(c)) 
        


def about(request):
    #Esto debería ser una funcion, aunque es provisional
    if request.user.is_authenticated():
        usuario = request.user.username
    else:
        usuario = 'login'
    template = get_template('about.html')
    c = Context({'usuario' : usuario})
    return HttpResponse(template.render(c))

@csrf_exempt
def usuario(request,usu):
    try:
        usuario = User.objects.get(username=usu)
    except User.DoesNotExist:
        return HttpResponse('<h1>404 Not Found Provisional: No existe el usuario</h1>')

    try:
        museos_de_usuario = Selec.objects.get(usuario=usuario)
        museos = museos_de_usuario.museo.all()
    except Selec.DoesNotExist:
        museos = None
    
    try:
        config = Conf.objects.get(usuario=usuario)
        titulo = config.titulo()
    except Conf.DoesNotExist:
        titulo = None
    template = get_template('usuario.html')
    
    if request.user.username == usu:
        user = request.user
    else:
        user = None
    c = Context({'title' : titulo,'events': museos, 'usuario' : usu, 'user' : user, 'userpage':usu})
    return HttpResponse(template.render(c))     
