from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from .models import Museo, Comentario, Conf, Selec
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.utils import timezone
from django.shortcuts import render_to_response


# Para comprobar si un usuario está autenticado o no
def check_user(request):
    if request.user.is_authenticated():
        usuario = request.user
    else:
        usuario = None
    return usuario

# Listado con los distritos para poder filtrar
def lista_distritos(museos):
    lista = list()
    for museo in museos:
        if museo.distrito not in lista:
            lista.append(museo.distrito)
    return(lista)

# Filtrar 5 primeros museos dependiendo de si son o no accesibles

def filtrar_museos(accesibles,first,last):
    if accesibles == True:
        museos = Museo.objects.annotate(num_comentarios=Count('comentario')).filter(accesibilidad = 1).order_by('-num_comentarios')[first:last]
    else:
        museos = Museo.objects.annotate(num_comentarios=Count('comentario')).order_by('-num_comentarios')[first:last]
    return museos

# Pasar de página
def paginas(pagina,ultimo):
    first = 0
    last = 0
    if pagina == ultimo:
        first = 0
        last = 5
    elif pagina < 5:
        first = 0
        if ultimo < 5:
            last = ultimo
        else:
            last = 5
    elif pagina + 5 > ultimo:
        first = pagina
        last = ultimo
    else:
        first = pagina
        last = pagina + 5
    return(first,last)

# Create your views here.
campos_xml = ('ID-ENTIDAD','NOMBRE','DESCRIPCION-ENTIDAD','HORARIO','TRANSPORTE','ACCESIBILIDAD',
'CONTENT-URL','NOMBRE-VIA','NUM','LOCALIDAD','CODIGO-POSTAL','DISTRITO',
'TELEFONO','FAX','EMAIL', 'TIPO')
def check_acces(access):
    if access == "1":
        check = True
    else:
        check = False
    return check

def get_museos():
    parse_file = urlopen('https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full')
    tree = ET.parse(parse_file)
    root = tree.getroot()
    museo_id = 1
    succes = True
    try:
        for element in root.iter():
            mylist = element.attrib.values()
            if campos_xml[0] in mylist:
                nuevo_museo = Museo(id=museo_id)
                museo_id += 1
            if campos_xml[1] in mylist:
                nuevo_museo.nombre = element.text
            if campos_xml[2] in mylist:
                nuevo_museo.descripcion = element.text
            if campos_xml[3] in mylist:
                nuevo_museo.horario = element.text
            if campos_xml[4] in mylist:
                nuevo_museo.transporte = element.text
            if campos_xml[5] in mylist:
                nuevo_museo.accesibilidad = check_acces(element.text)
            if campos_xml[6] in mylist:
                nuevo_museo.url = element.text
            if campos_xml[7] in mylist:
                nuevo_museo.calle = element.text
            if campos_xml[8] in mylist:
                nuevo_museo.numero = element.text
            if campos_xml[9] in mylist:
                nuevo_museo.localidad = element.text
            if campos_xml[10] in mylist:
                nuevo_museo.codigo_postal = element.text
            if campos_xml[11] in mylist:
                nuevo_museo.distrito = element.text
            if campos_xml[12] in mylist:
                nuevo_museo.telefono = element.text
            if campos_xml[13] in mylist:
                nuevo_museo.fax = element.text
            if campos_xml[14] in mylist:
                nuevo_museo.email = element.text
            if campos_xml[15] in mylist:
                nuevo_museo.save()
    except:
        succes = False
    return succes

def info_museo(museo):
    info = '<br><strong>' + museo.nombre + '</strong><br>'
    info += '<strong>Descripcion: </strong>' + museo.descripcion + '<br>'
    info += '<strong>Horario: </strong>' + museo.horario + '<br>'
    info += '<strong>Transporte: </strong>' + museo.transporte + '<br>'
    info += '<strong>Accesible: </strong>'
    if museo.accesibilidad == '1':
        info += 'Si<br>'
    else:
        info += 'No<br>'
    info += '<strong>URL: </strong>' + '<a href=' + museo.url + '>' + museo.url + '</a><br>'
    info += '<strong>Direccion: </strong>c/' + museo.calle + ', nº' + museo.numero + ', '
    info +=  museo.distrito + ', ' + museo.codigo_postal + ', ' + museo.localidad +'<br>'
    info += '<strong>Telefono: </strong>' + museo.telefono + ', '
    info += '<strong>Fax: </strong>' + museo.fax + ', '
    info += '<strong>Email: </strong>' + museo.email + '<br>'
    return info


@csrf_exempt
def my_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        template = get_template('error.html')
        login_error = 'Te estas intentando loggear con un nombre de usuario y contraseña erroneos<br>'
        c = Context({'error':login_error})
        login_error += 'Vuelve a intentarlo o registrate si aun no lo has hecho'
        return HttpResponse(template.render(c))

@csrf_exempt
def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def my_registration(request):
    template = get_template('registration.html')
    if request.method == 'GET':
        return HttpResponse(template.render())
    elif request.method == 'POST':
        register_username = request.POST['username']
        register_password = request.POST['password']
        try:
            check = User.objects.get(username=register_username)
            c = Context({'check':check})
            return HttpResponse(template.render(c))
        except User.DoesNotExist:
            user = User.objects.create_user(username=register_username,password=register_password)
            user.save()
            user = authenticate(username=register_username, password=register_password)
            login(request, user)
            titulo_defecto = 'Pagina de ' + user.username
            conf = Conf(usuario=user,titulo=titulo_defecto)
            return HttpResponseRedirect('/')


@csrf_exempt
def barra(request):
    metodo = ''
    museos_all = Museo.objects.all()
    usuario = check_user(request) #Deberia cambiarlo a visitante
    config = Conf.objects.all()
    template = get_template('principal.html')
    c = Context({})
    if request.method == 'GET':
        if request.GET and request.GET['barra'] == 'Cargar':
            succes = get_museos()
            if not succes:
                template = get_template('error.html')
                load_error = 'No se han podido cargar los museos'
                return HttpResponse(template.render(Context({'error':load_error})))
            return HttpResponseRedirect('/')
        else:
            accesibles = False
            metodo = 'POST'
            museos = filtrar_museos(accesibles,0,5)
            c = Context({'objects': museos_all,'configurations':config, 'events' : museos,
            'page': 5, 'method' : metodo, 'user' : usuario, 'check': accesibles})

    elif request.method == 'POST':
        if request.POST['barra'] == 'Accesibles':
            metodo = 'GET'
            accesibles = True
            museos = filtrar_museos(accesibles,0,5)
            pagina = 5
        else:
            num_museos = 0
            accesibles = request.POST['accesible']
            if accesibles == 'False': #OJO, es un string, no un boolean
                num_museos = Museo.objects.all().count()
                accesibles = False
                metodo = 'POST'
            else:
                num_museos = Museo.objects.filter(accesibilidad = 1).count()
                accesibles = True
                metodo = 'GET'

            pagina = int(request.POST['barra'])
            first,last = paginas(pagina,num_museos)
            museos = filtrar_museos(accesibles,first,last)
            pagina = last

        c = Context({'objects': museos_all,'configurations':config,'events' : museos, 'page' : pagina,
        'method':metodo, 'user' : usuario, 'check' : accesibles})

    return HttpResponse(template.render(c))


@csrf_exempt
def museos(request):
    usuario = check_user(request)
    museos = Museo.objects.all()
    distritos = lista_distritos(museos)
    template = get_template('museos.html')

    if request.method == 'POST':
        distrito = request.POST['distrito']
        museos_filtrados = Museo.objects.filter(distrito = distrito)
    else:
        #Por defecto, el primer distrito de la lista
        museos_filtrados = Museo.objects.filter(distrito = distritos[0])
    c = Context({'districts' : distritos, 'filt_events' : museos_filtrados,'user' : usuario})
    return HttpResponse(template.render(c))

@csrf_exempt
def museo(request,num):
    respuesta = ''
    usuario = check_user(request)

    try:
        museo = Museo.objects.get(id=int(num))
        comentarios = Comentario.objects.filter(museo=museo)
        if request.method == 'GET':
            respuesta = info_museo(museo)
        elif request.method == 'POST':
            if request.POST['museo']=='Like':
                try:
                    museos_de_usuario = Selec.objects.get(usuario=request.user)
                    if museo not in museos_de_usuario.museo.all():
                        museos_de_usuario.museo.add(museo)
                except Selec.DoesNotExist:
                    nuevo_selec = Selec(usuario = request.user,fecha = timezone.now())
                    nuevo_selec.save()
                    nuevo_selec.museo.add(museo)
                return HttpResponseRedirect('/museo/'+ num)
            else:
                comentario = Comentario(autor = request.POST['usuario'],
                texto = request.POST['museo'], museo = museo, fecha = timezone.now())
                comentario.save()
                return HttpResponseRedirect('/museo/' + num)
    except Museo.DoesNotExist:
            template = get_template('error.html')
            museum_error = 'No existe el museo al que intenta acceder'
            return HttpResponse(template.render(Context({'error': museum_error})))

    template = get_template('museo.html')
    c = Context({'user' : usuario,'info' : respuesta, 'comments': comentarios})
    return HttpResponse(template.render(c))



def about(request):
    usuario = check_user(request)
    template = get_template('about.html')
    c = Context({'user' : usuario})
    return HttpResponse(template.render(c))

@csrf_exempt
def usuario(request,usu):
    user = request.user
    try:
        usuario = User.objects.get(username=usu)
    except User.DoesNotExist:
        template = get_template('error.html')
        user_error = 'No existe el usuario ' + usu
        return HttpResponse(template.render(Context({'error':user_error})))

    try:
        museos_de_usuario = Selec.objects.get(usuario=usuario)
        museos = museos_de_usuario.museo.all()
    except Selec.DoesNotExist:
        museos = None

    try:
        config = Conf.objects.get(usuario=usuario)
    except Conf.DoesNotExist:
        titulo = 'Página de ' + usu
        config = Conf(usuario=usuario,titulo=titulo)
        config.save()


    if request.method == 'POST':
        if request.POST['cambio'] == 'Titulo':
            config.titulo = request.POST['titulo']
        elif request.POST['cambio'] == 'Fuente':
            config.fuente = request.POST['fuente']
        elif request.POST['cambio'] == 'Fondo':
            config.color = request.POST['fondo']
        else:
            pass
        config.save()
    template = get_template('usuario.html')
    if user == usuario:
        pass
    else:
        usuario = None
    try:
        user_config = Conf.objects.get(usuario = user)
        user_color = user_config.color
        user_size = user_config.fuente
    except:
        user_color = 'gainsboro'
        user_size = '15px'
    # Si el visitante de la pagina no es el usuario, no se le ofrecen las modificaciones
    c = Context({'title': config.titulo,'events': museos, 'user' : user,
    'userpage':usuario, 'color':user_color, 'size':user_size})
    return HttpResponse(template.render(c))

def usuario_xml(request,usu):
    template = get_template('usuario.xml')
    try:
        user_to_xml = User.objects.get(username=usu)
        selec_to_xml = Selec.objects.get(usuario=user_to_xml)
        museos_to_xml = selec_to_xml.museo.all()
        c = Context({'user':user_to_xml,'user_selecs':museos_to_xml})
        return HttpResponse(template.render(c),content_type="text/xml")
    except User.DoesNotExist:
        template = get_template('error.html')
        user_error = 'No existe el usuario ' + usu
        return HttpResponse(template.render(Context({'error':user_error})))
