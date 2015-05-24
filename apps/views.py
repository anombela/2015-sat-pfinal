# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect)
from django.views.decorators.csrf import csrf_exempt
from models import (Actividad,Usuario,Actividad_User, 
                    Variablescss, Comentario , Comments)
import xmlparsersax
import datetime 
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import redirect

from django.contrib.auth.forms import (UserCreationForm, 
										AuthenticationForm)
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from BeautifulSoup import BeautifulSoup
import urllib2

# Create your views here.

def addusers():  ##esto se ejecuta cada vez que se ejecuta la aplicacion y actualiza los usuarios que hay
	users = User.objects.all()
	usrs = Usuario.objects.all()
	for user in users:
		add=True
		for us in usrs:
			if str(user) == us.user:
				add=False
				break
		if add:	
			userr = Usuario(user=str(user), title="pagina de "+str(user), descripcion="esta es la pagina personal de "+str(user))
			userr.save()
			
addusers()

def formlog(request):
	estado = ""
	if request.user.is_authenticated():
		estado += ("<h6>Usuario actual: <a href='/"+ request.user.username +"'>" + request.user.username+"</a>"+
					" <p>______<a href='/logout'>Logout</a>______</p></h6>")

	else:
		estado += ('<form id="form2" method="POST" class="contact_us" action="/ingresar">'+
    				'<p><label>Username'+
    				'<input type="text" class="fields_contact_us" name="username" />'+
   					'</label>'+
   					'<label>Password'+
   					'<input type="text" class="fields_contact_us" name="password" />'+
					'</label>'+
					 '<label>'+
    				'<input type="submit" class="submit_button_contact" name="Submit3" value="Login" />'+
    				'</label></p></form>')
	

	return estado

def usuarios():
	usuarios=User.objects.all()
	salida = "<h6>"
	for usuario in usuarios:
		salida+= "<li>"+str(usuario)+\
					"<dd><a href='/"+str(usuario)+"'>-Pagina personal</a></dd>"+\
					"<dd><a href='/"+str(usuario)+"/rss'>-canal rss </a></li>"



	return salida + "</h6>"

def getactividades(request):

	actividades = Actividad.objects.all()
	fechamod = datetime.datetime.today()
	xmlparsersax.getparse(actividades,fechamod)

	actividades = Actividad.objects.all()  #ya actualizadas
	for actividad in actividades:
		if actividad.fechamod!=fechamod:
			actividad.delete()

	return redirect("/todas")

def cleanall(request):
    Actividad.objects.all().delete() 
    return redirect("/todas")

def printactivities(actividad, num):

	
	salida=""
	titulocorto = actividad.titulo
	if len(actividad.titulo)>58:
		titulocorto = actividad.titulo[0:55] +" ..."

	
	salida += '<div class="date_box"><div class="date_box_month">activ</div>'
	salida += '<div class="date_box_day">'+str(num)+'</div></div>'

	salida += "<dt><h3><a href='/actividad/"+str(actividad.id)+"'>"+ titulocorto + "</a></h3></dt>"
	salida += "<blockquote><dd>- Tipo: " + actividad.tipo + "</dd>"
	salida += "<dd>- Precio: " + actividad.precio + "</dd>"
	salida += "<dd>- Fecha: " + str(actividad.fecha) + "</dd>"
	salida += "<dd>- Hora: " + str(actividad.hora) + "</dd>"
	salida += "<dd>- Duracion: " + str(actividad.duracion) + "</dd>"
	salida += "<div align='right'><a href=" + actividad.urlinfo +"> Click para mas informacion</a></div>"

	return salida

def beautiful(url):
	
	salida="<dl><dt><li>Informacion adicional:</li></dt><br>"

	try:
		soup = BeautifulSoup(urllib2.urlopen(url).read())
		out = str(soup.find('div',id="tabContent_0").find('strong'))

		url = "http://www.madrid.es" + out.split('"')[1]
		url = url.split("amp;")
		url = url[0] + url[1]+url[2]
		soup = BeautifulSoup(urllib2.urlopen(url).read())
		tags = soup.find('div', id="contenedor31").findAll('div', {'class':'parrafo'})
	
		for tag in tags:
			tags2=tag.findAll('p')
			for tag2 in tags2:
				salida+= "<dd>- " + str(tag2).split("<p>")[1].split("</p>")[0].decode('utf-8')  + "</dd>"
	except:
		salida +=""
	return salida

@csrf_exempt
def showall(request):


	actividades=Actividad.objects.order_by("fecha")

	actividades = Actividad.objects.all()
	numactiv = 0
	fechamodificacion=0
	for actividad in actividades:
		fechamodificacion = actividad.fechamod
		numactiv = numactiv+1

	try:
	    titulo = request.POST["titulo"]
	    if titulo :
	        actividades=actividades.filter(titulo=titulo)
	    precio = request.POST["precio"]
	    if precio:
	    	actividades=actividades.filter(precio=precio)
	    fecha = request.POST["fecha"]
	    if fecha:
	    	actividades=actividades.filter(fecha=fecha)
	    duracion = request.POST["duracion"]
	    if duracion:
	    	actividades=actividades.filter(duracion = duracion)
        
	except:
		salida =""
		

	salida = "<h5>Todas las actividades disponibles</h5>"
	salida += "<p><h6>---------Es posible filtrar por varios campos simultaneamente----------"
	salida += '<form action="" method="POST">\n'
	salida += 'Titulo: <input type="text" name="titulo">\n'
	salida += 'Fecha: <input type="text" name="fecha">\n'
	salida += '<br>Precio: <input type="text" name="precio">\n'
	salida += 'Duracion: <input type="text" name="duracion">\n'
	salida += '<br><input type="submit" value="Buscar">\n'
	salida += '</form></h6><br>'

	if request.user.is_authenticated():
		usuario = Usuario.objects.get(user=request.user.username)
		misactividades = usuario.actividades.all()
		nummisactv = 0
		for miactividad in misactividades:
			nummisactv = nummisactv +1

		salida += "<h6>Ultima actualizacion: "+str(fechamodificacion) 
		salida += "<br>Numero actividades disponibles: " + str(numactiv) 
		salida += "<br>Numero actividades en mi pagina: "+str(nummisactv) + "</h6><p>"

	num = 0
	for actividad in actividades:
		num = num + 1

		salida += printactivities(actividad, num)

		if request.user.is_authenticated():
			try:
				usuario=Usuario.objects.get(actividades__titulo = actividad.titulo, user = request.user.username)
				salida+= "--Actividad disponible en pagina personal-->"
				salida += '<form action="/delactividad/'+str(actividad.id)+'" style="display:inline" method="GET">'
				salida += '<input type="submit" value="Eliminar">'
				salida += '</form>'

			except:

				salida += '<dd><form action="/addactividad/'+str(actividad.id)+'" method="GET">\n'
				salida += '<input type="submit" value="Annadir actividad a pagina personal">\n'
				salida += '</form></dd>'


		salida += printpuntuacion(actividad)
		salida += "</blockquote>"
	if not actividades:
		salida += "<blockquote><h1>Lista vacia</h1></blockquote>"

	users = usuarios()
	login = formlog(request)
	inicio = '<li id="active"><a href="/" id="current">Inicio</a></li>'

	actualizar= ""
	if request.user.is_authenticated():
		actualizar = "<li><a href='/update'>Actualizar</a></li>"+\
					"<li><a href='/clean'>Borrar</a></li>"
	# 1. Indicar plantilla
	template = get_template("index.html")
	# 2. Marcar contexto -> contenido: salida
	c = Context({'contenido': salida, 'login': login,  'usuarios': users, 'inicio': inicio, 'actualizar': actualizar})
	# 3. Renderizar
	lorenderizado = template.render(c)

	return HttpResponse(lorenderizado)

@csrf_exempt
def showhome(request):

	actividades=Actividad.objects.order_by("fecha","hora")

	t = str(datetime.datetime.today()).split(" ")
	fecha = t[0].split("-")
	hora = t[1].split(":")
	fecha = datetime.date(int(fecha[0]),int(fecha[1]),int(fecha[2]))
	hora = datetime.time(int(hora[0]),int(hora[1]))

	num = 0
	salida = "<h5>10 actividades mas proximas</h5>"

	for actividad in actividades:
		if fecha>actividad.fecha:
			continue
		elif fecha == actividad.fecha and hora>actividad.hora:
			continue

		if num == 10:
			break
		num = num + 1
		titulocorto = actividad.titulo
		if len(actividad.titulo)>58:
			titulocorto = actividad.titulo[0:55] +" ..."

		salida += '<br><div class="date_box"><div class="date_box_month">activ</div>'
		salida += '<div class="date_box_day">'+str(num)+'</div></div>'
		salida += "<h3><a href='/actividad/"+str(actividad.id)+"'>"+ titulocorto + "</a></h3></br>"

	if not actividades:
		salida += "<h1>Lista vacia</h1>"



	salida += "<h5>Paginas personales disonibles</h5>"
	us=Usuario.objects.all()
	salida += "<p><h6>"
	for usuario in us:
		salida+= "<li><a href='/"+str(usuario.user)+"'>"+usuario.title+"</a>"+\
					"<dd>- "+usuario.user+"</dd></li>" + \
					"<dd>- "+usuario.descripcion+"</dd></li><p>"


	salida += "</h6></p>"
	login = formlog(request)
	users = usuarios()
	rss = "<li><a href='/rss'>RSS</a></li>"

	# 1. Indicar plantilla
	template = get_template("index.html")
	# 2. Marcar contexto -> contenido: salida
	c = Context({'contenido': salida, 'login': login, 'usuarios': users, 'rss': rss})
	# 3. Renderizar
	lorenderizado = template.render(c)

	return HttpResponse(lorenderizado)

@csrf_exempt
def showactividad(request, recurso):

	actividad=Actividad.objects.get(id=recurso)
	num=0
	salida = printactivities(actividad, num)
	salida += beautiful(actividad.urlinfo)

	salida += printpuntuacion(actividad)
	salida += "</blockquote>"
	salida += '<form action="/comentario/'+str(actividad.id)+'" method="POST">'+\
			'<textarea name="comentario" cols=40 rows=4>I urge you to see it.</textarea>'+\
			'<input type="submit" value="Publish"></form>'

	login = formlog(request)
	inicio = '<li id="active"><a href="/" id="current">Inicio</a></li>'
	# 1. Indicar plantilla
	template = get_template("index.html")
	# 2. Marcar contexto -> contenido: salida
	c = Context({'contenido': salida, 'login': login, 'inicio': inicio})
	# 3. Renderizar
	lorenderizado = template.render(c)

	return HttpResponse(lorenderizado)



def delactividad(request, recurso):

	actividadoriginal= Actividad.objects.get(id = recurso)
	usuario = Usuario.objects.get(user = request.user.username)


	actividades = usuario.actividades.all()
	for actividad in actividades:
		if actividad.titulo == actividadoriginal.titulo:
			actividad.delete()
			

	return HttpResponseRedirect("/" + request.user.username)


def addactividad(request, recurso):

	fechaadd = datetime.datetime.today()

	actividad = Actividad.objects.get(id=recurso)

	a=Actividad_User(titulo=actividad.titulo, fecha=actividad.fecha, urlinfo = actividad.urlinfo, fechaadd = fechaadd)
	a.save()

	usuario = Usuario.objects.get(user=request.user.username)

	usuario.actividades.add(a)
	usuario.save()

	return HttpResponseRedirect("/actividad/"+recurso)


def usuario(request, recurso, pagina):

	esta = False
	usuarioss = User.objects.all()
	for usuario in usuarioss:
		if str(usuario) == recurso:
			esta=True
	
	if esta:
		titulo = "<h5>Pagina personal de "+recurso 
		if recurso==request.user.username and request.user.is_authenticated():
			titulo += "-online"
			titulo += "<br> -Titulo: " + Usuario.objects.get(user = recurso).title


		titulo += "</h5>"

		salida = ""
		usuario = Usuario.objects.get(user=recurso)
		actividades = usuario.actividades.all()
		num = 0

		if pagina== "":
			pagina = str(1)
		
		fin = int(pagina) * 10  #acaba en 10 or ejemplo
		inicio= fin - 10   #comienza en 1 por ejemplo

		haymas=False
		haymenos=False

		for actividad in actividades:

			num=num+1
			if num <= inicio:
				haymenos=True
				continue
			elif num >fin:
				haymas=True
				break

			
			activida = Actividad.objects.filter(titulo = actividad.titulo)
			activida = activida[0]

			titulocorto = actividad.titulo
			if len(actividad.titulo)>58:
				titulocorto = actividad.titulo[0:55] +" ..."

			salida += '<div class="date_box"><div class="date_box_month">activ</div>'
			salida += '<div class="date_box_day">'+str(num)+'</div></div>'
			salida += "<h3><a href='/actividad/"+str(activida.id)+"'>"+titulocorto + "</a></h3>"
		
			salida += "<blockquote><dd>- Fecha: " + str(actividad.fecha) + "</dd>"
			salida += "<dd>- Elegida en: " + str(actividad.fechaadd) + "</dd>"

			if request.user.is_authenticated():
			
				actvoriginal = Actividad.objects.filter(titulo = actividad.titulo)
				actvoriginal = actvoriginal[0]
				salida += '<form action="/delactividad/'+str(actvoriginal.id)+'" method="GET">'
				salida += '<input type="submit" value="Eliminar">'
				salida += '</form>'

			salida += "</blockquote>"
			

		if not actividades:
			salida += "<br><h2>No hay actividades</h2></br>"

		if haymenos:
			salida += '<form action="/' + recurso + '/' + str(int(pagina) - 1) + '" style="display:inline" method="GET">\n'
			salida += '<input type="submit" value="<<">'
			salida += '</form>'

		if haymas:
			salida += '<form action="/' + recurso + '/' + str(int(pagina) + 1) + '" style="display:inline" method="GET">\n'
			salida += '<input type="submit" value=">>">'
			salida += '</form>'


		salida += "<h5>Comentarios de " + recurso + "</h5>"
		salida += "<p><h6>"

		if recurso==request.user.username:
			comentarios = Comments.objects.filter(user = request.user.username)
			
			for comentario in comentarios:

				comentariostitulo = comentario.comments.filter(tituloactividad = comentario.titulo)



				try:  ##algunas veces aparacen dos actividades exactamente iguales
					actividad = Actividad.objects.get(titulo=comentario.titulo)
				except:
					actividad = Actividad.objects.filter(titulo=comentaro.titulo)
					actividad = actividad[0]


				
				#return HttpResponse(comentario.titulo)
				salida+= "<li><a href='/actividad/"+str(actividad.id)+"'>"+comentario.titulo+"</a>"

				numcomment=0
				for c in comentariostitulo:
					numcomment=numcomment+1
					salida += "<dd>- Comentario "+str(numcomment)+":  "+c.comentario+"</dd></li>"
				
		else:
			salida +="No hay comentarios de actividades"

		salida += "</h6></p>"

		apariencia = ""
		if request.user.is_authenticated():
			if recurso==request.user.username:
				salida += putcss(recurso)
				apariencia = formapariencia()


		login = formlog(request)
		users = usuarios()
		inicio = '<li id="active"><a href="/" id="current">Inicio</a></li>'

		# 1. Indicar plantilla
		template = get_template("index.html")
		# 2. Marcar contexto -> contenido: salida
		c = Context({'contenido': salida, 'login': login, 'usuarios': users, 'titulo': titulo, 'apariencia': apariencia, 'inicio': inicio})
		# 3. Renderizar
		lorenderizado = template.render(c)
		return HttpResponse(lorenderizado)
	else:
		return HttpResponse("Usuario "+recurso+ " no tiene pagina personal  <br><a href='/'>Inicio</a>")


def nuevo_usuario(request):
    if request.method=='POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
    return render_to_response('nuevousuario.html',{'formulario':formulario}, context_instance=RequestContext(request))


@csrf_exempt
def ingresar(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:

                if acceso.is_active:
                    login(request, acceso)
                    
	return HttpResponseRedirect("/")

def salir(request):
	logout(request)
	return HttpResponseRedirect("/")


def cleancss(request):

	estilos = Variablescss.objects.filter(user=request.user.username)
	for estilo in estilos:
		estilo.delete()

	return HttpResponseRedirect("/"+ request.user.username)
	

def putcss(user):

	usuario = Usuario.objects.get(user=user)
	estilos = usuario.css.all()
	salida=""
	for estilo in estilos:

		if estilo.name == "right":
			salida += "<style>#right {color:" + estilo.colorletra+"; font-size: " +\
					 estilo.tamannoletra + "em;background-color: " + estilo.colorfondo + ";}</style>"
		elif estilo.name == "footer":
			salida += "<style>#footer {color:" + estilo.colorletra+"; font-size: " +\
					 estilo.tamannoletra + "em;background-color: " + estilo.colorfondo + ";}</style>"
		elif estilo.name == "h6":
			salida += "<style> h6 {color:" + estilo.colorletra+"; font-size: " +\
					 estilo.tamannoletra + "em;background-color: " + estilo.colorfondo + ";}</style>"
		elif estilo.name == "link":
			salida += "<style>a:link {color:" + estilo.colorletra+"; font-size: " +\
					 estilo.tamannoletra + "em;background-color: " + estilo.colorfondo + ";}</style>"
		elif estilo.name == "container":
			salida += "<style>#container {color:" + estilo.colorletra+"; font-size: " +\
					 estilo.tamannoletra + "em;background-color: " + estilo.colorfondo + ";}</style>"

	return salida


def formapariencia():
	salida = ( '<h4>Apariencia</h4>'
		'<h6><form action="/apariencia" method="post" accept-charset="utf-8">'
        '<p><select name="id" id="ids" class="v3" >'
        '<option value="right" selected="selected">Centro</option>'
        '<option value="h6" selected="selected">Menus</option>'
        '<option value="link" selected="selected">Links</option>'
        '<option value="footer" selected="selected">Pie de pagina</option>'#container
        '<option value="container" selected="selected">container</option>'
        '</select></p>'
        '<p><select name="tipo" id="tipos" class="v4" >'
        '<option value="colorletra" selected="selected">ColorLetra</option>'
        '<option value="tamannoletra" selected="selected">TamañoLetra</option>'
        '<option value="colorfondo" selected="selected">Colorfondo</option>'
        '</select></p>'
        '<p><input type="text" name="valor"></p>'

        '<p><input type="submit" value="Cambiar"></p>'
        '</form>'

        '<form action="/cleancss" method="GET">'
        '<input type="submit" value="Resetear formato"></form></h6>')
	return salida

@csrf_exempt
def formato(request):

	global ide , variable
	if request.method == 'POST':
		ide = request.POST['id']
		tipo = request.POST['tipo']
		variable= request.POST['valor']

	try:
		q=Variablescss.objects.get(user=request.user.username,name=ide)
		if tipo == "colorletra":
			q.colorletra=variable
		elif tipo == "tamannoletra":
			q.tamannoletra=variable
		elif tipo == "colorfondo":
			q.colorfondo=variable
		q.save()


	except:
		if tipo == "colorletra":
			a = Variablescss(user=request.user.username, name= ide, colorletra=variable)
		elif tipo == "tamannoletra":
			a = Variablescss(user=request.user.username, name= ide, tamannoletra=variable)
		elif tipo == "colorfondo":
			a = Variablescss(user=request.user.username, name= ide, colorfondo=variable)
		a.save()

		usuario = Usuario.objects.get(user=request.user.username)
		usuario.css.add(a)
		usuario.save()

	return HttpResponseRedirect("/"+request.user.username)


def createrss(request, user):

	usuario = Usuario.objects.get(user=user)
	actividades = usuario.actividades.all()

	salida = '<?xml version="1.0" encoding="ISO-8859-1" ?>\n'+\
				'<rss version="2.0">\n' +\
				'\t<channel>\n' +\
				'\t\t<title>Canal RSS de '+user+'</title>\n'

	for actividad in actividades:

		try:  ##algunas veces aparacen dos actividades exactamente iguales
			actividad = Actividad.objects.get(titulo=actividad.titulo)
		except:
			actividad = Actividad.objects.filter(titulo=actividad.titulo)
			actividad = actividad[0]
		salida +=  "\t<item>\n" + \
					"\t\t<titulo>"+actividad.titulo +"</titulo>\n" +\
					"\t\t<id>"+ str(actividad.id) +"</id>\n" +\
					"\t\t<tipo>"+actividad.tipo +"</tipo>\n" +\
					"\t\t<precio>"+actividad.precio +"</precio>\n" +\
					"\t\t<fecha>"+ str(actividad.fecha) +"</fecha>\n"+\
					"\t\t<hora>"+ str(actividad.hora) +"</hora>\n"+\
					"\t\t<duracion>"+ str(actividad.duracion)+"</duracion>\n"+\
					"\t\t<eslargo>"+ str(actividad.eslargo) +"</eslargo>\n"+\
					"\t</item>\n"
					#"\t\t<url>"+ str(actividad.urlinfo) +"</url>\n"+\

	return HttpResponse(salida+'\t</channel>\n</rss>\n', content_type='rss')


def rsshome(request):

	actividades=Actividad.objects.order_by("fecha","hora")

	t = str(datetime.datetime.today()).split(" ")
	fecha = t[0].split("-")
	hora = t[1].split(":")
	fecha = datetime.date(int(fecha[0]),int(fecha[1]),int(fecha[2]))
	hora = datetime.time(int(hora[0]),int(hora[1]))


	salida = '<?xml version="1.0" encoding="ISO-8859-1" ?>\n'+\
				'<rss version="2.0">\n' +\
				'\t<channel>\n' +\
				'\t\t<title>Canal RSS de la pagina principal </title>\n'

	
	num = 0
	for actividad in actividades:
		if fecha>actividad.fecha:
			continue
		elif fecha == actividad.fecha and hora>actividad.hora:
			continue

		if num == 10:
			break
		num = num + 1

		try:  ##algunas veces aparacen dos actividades exactamente iguales
			actividad = Actividad.objects.get(titulo=actividad.titulo)
		except:
			actividad = Actividad.objects.filter(titulo=actividad.titulo)
			actividad = actividad[0]

		salida +=  "\t<item>\n" + \
					"\t\t<titulo>"+actividad.titulo +"</titulo>\n" +\
					"\t\t<id>"+ str(actividad.id) +"</id>\n" +\
					"\t\t<tipo>"+actividad.tipo +"</tipo>\n" +\
					"\t\t<precio>"+actividad.precio +"</precio>\n" +\
					"\t\t<fecha>"+ str(actividad.fecha) +"</fecha>\n"+\
					"\t\t<hora>"+ str(actividad.hora) +"</hora>\n"+\
					"\t\t<duracion>"+ str(actividad.duracion)+"</duracion>\n"+\
					"\t\t<eslargo>"+ str(actividad.eslargo) +"</eslargo>\n"+\
					"\t</item>\n"
					#"\t\t<url>"+ str(actividad.urlinfo) +"</url>\n"+\

	return HttpResponse(salida+'\t</channel>\n</rss>\n', content_type='rss')



def puntuacion(request, recurso):


	actividad = Actividad.objects.get(id=recurso)
	actividad.puntuacion = actividad.puntuacion + 1
	actividad.save()

	return HttpResponseRedirect("/todas")

def printpuntuacion(actividad):

	salida = '<div align="right">puntuacion: '+ str(actividad.puntuacion)
	salida += '&nbsp<form action="/puntuacion/'+str(actividad.id)+'" style="display:inline" method="GET">'
	salida += '<input type="submit" value="+1">'
	salida += '</form>'+  '</div>'
	return salida

@csrf_exempt
def putcomment(request, recurso):

	actividad = Actividad.objects.get(id = recurso)

	comentario =  Comentario(tituloactividad=actividad.titulo, comentario=request.POST['comentario'])
	comentario.save()

	try:
		usuario = Comments.objects.get(user=request.user.username, titulo =actividad.titulo)
	except:
		usuario = Comments(user=request.user.username, titulo =actividad.titulo)
		usuario.save()

	usuario.comments.add(comentario)
	usuario.save()

	return HttpResponseRedirect("/")


def ayudas(request):

	salida ="<blockquote>"

	salida += "En esta pagina se muestra la ayuda sobre el funcinamiento basico de la aplicacion web 'Delorean':"+\
			"<br>---Principales recursos disponibles:---<br>" + \
			"<br><li>/ : muestra la pagina principal de la aplicacion, en ella se muestran las 10 actividades mas proximas en el tiempo y las paginas personales disponibles.</br>" + \
			"<br><li>/usuario : pagina personal del usuario donde se muestran sus actividades selecionadas, los parametros css y su pagina personal.</br>" + \
			"<br><li>/actividad/id : pagina de cada actividad especifica donde se muestra informacion adicional y cada usuario registrado o no puede comentar sobre ella</br>" + \
			"<br><li>/usuario/rss: canal rss de las incidencias elegidas por el usuario</br>" + \
			"<br><li>/ayuda : muestra esta pagina </br>" + \
			"<br><li>/todas : pagina que muestra todas las actividades disponibles, ademas se puede filtrar la busqueda de estas gracias a el formularioexistente.</br>" + \
			"<br>---Principales botones disponibles:---</br>" + \
			"<br><li>Inicio: boton que accede al recurso '/'</br>" + \
			"<br><li>Todas: boton que accede al recurso '/todas'</br>" + \
			"<br><li>Ayuda: boton que accede al recurso '/ayuda'</br>" + \
			"<br><li>RSS: boton que accede a el rss de la pagina de inicio</br>" + \
			"<br><li>Actualizar: boton para actualizar las actividades disponibles (solo disponible de manera privada).</br>" + \
			"<br><li>Borrar: boton para eliminar por completo las actividades disponibles (solo disponible de manera privada).</br>" + \
			"<br>---Diferentes menus:---</br>" + \
			"<br><li>Menu de opciones: en el se pueden acceder a los botones principales</br>" + \
			"<br><li>Usuario: menu en el que se muestra el estado actual de usuario, si hay alguien logeado  le mostrara la opcion de salir, de lo contrario mostrara un formulario para logearse.</br>" + \
			"<br><li>Usuarios registrados: muestra los usuarios registrados  en la base de datos, de cada uno de ellos muestra un enlace a la pagina personal y al canal rss.</br>" + \
			"<br><li>Apariencia:  menu para cambiar la apariencia de la pagina personal (solo usuarios logeados), utiliza un formulario en el que se pueden elegir las opciones. Tambien dispone de un boton para resetear el formato</br>" + \
			"<br>---Datos de interes:---</br>" + \
			"<br><li>se podradar +1 a cualquier actividad estando logeado o no, la cuenta de esto se vera en cada actividad</br>" + \
			"<br><li>en la pagina todas, si se esta logeado aparecera un boton para annadir a la pagina personal una actividad o si ya esta annadida se podrá eliminar</br>" + \
			"<br><li>en la pagina personal de un usuario logeado se mostraran ademas los comentarios que ha realizado en cada actividad</br>"

	salida +="</blockquote>"

	login = formlog(request)
	users = usuarios()
	inicio = '<li id="active"><a href="/" id="current">Inicio</a></li>'
	titulo = "<h5>Pagina de ayuda</h5>"
		
	# 1. Indicar plantilla
	template = get_template("index.html")
	# 2. Marcar contexto -> contenido: salida
	c = Context({'contenido': salida, 'login': login, 'usuarios': users, 'titulo': titulo, 'inicio': inicio})
	# 3. Renderizar
	lorenderizado = template.render(c)
	return HttpResponse(lorenderizado)
