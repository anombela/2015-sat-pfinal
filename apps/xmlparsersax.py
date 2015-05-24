from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from models import Actividad
import datetime


actividades=""
fechamod=""

def inicializar(self):
            self.titulo = ""
            self.precio = ""
            self.tipo = ""
            self.fecha = ""
            self.hora = ""
            self.eslargo = 0 #por si no encuentra alguno
            self.urlinfo = ""
            self.duracion = ""

class myContentHandler (ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.CurrentData = ""
        self.theContent = ""
        inicializar(self)   #inicializa todas las variables
        self.contador = 0
        self.contador2 = 0

    def startElement(self, name, attrs):

        if name == 'contenido':
            if self.contador ==200000:
                self.contador = self.contador
            else:
                self.inItem = True
                self.contador = self.contador+1
        elif self.inItem:
            if name == 'atributo':
                self.inContent = True
                self.CurrentData = attrs['nombre']

    def endElement(self, name):
        if name == 'contenido':
            if self.contador2 ==200000:
                self.contador2 = self.contador2
            else:
                
                self.name = ""
                self.inItem = False
                self.contador2 = self.contador2+1
        elif self.inItem:
            if name == 'atributo' and self.CurrentData == 'TITULO':
                self.titulo = self.theContent
                self.inContent = False
                self.theContent = ""
            if name == 'atributo' and self.CurrentData == 'PRECIO':
                self.precio = self.theContent
                self.inContent = False
                self.theContent = ""
            if name == 'atributo' and self.CurrentData == 'FECHA-EVENTO':
                self.fecha = self.theContent.split(" ")[0]  ##quito la hora de aqui por que siempre es 00:00
                self.inContent = False
                self.theContent = ""
            if name == 'atributo' and self.CurrentData == 'HORA-EVENTO':
                self.hora = self.theContent
                self.inContent = False
                self.theContent = ""
            if name == 'atributo' and self.CurrentData == 'FECHA-FIN-EVENTO':
                self.duracion = self.theContent
                self.inContent = False
                self.theContent = ""
            if name == 'atributo' and self.CurrentData == 'EVENTO-LARGA-DURACION':
                self.eslargo = int(self.theContent)
                self.inContent = False
                self.theContent = ""
            if name == 'atributo' and self.CurrentData == 'CONTENT-URL-ACTIVIDAD':
                self.urlinfo = self.theContent 
                self.inContent = False
                self.theContent = ""
            if name == 'atributo' and self.CurrentData == 'TIPO':
                self.tipo = self.theContent

                if self.precio == "":
                    self.precio = "gratuito"

                if len(self.fecha)==10 and len(self.hora)==5: #aveces da una fecha mal, solo guarda si es correcta

                    add=True
                    for actividad in actividades:
                        if actividad.titulo == self.titulo:
                            actividad.fechamod = fechamod #pone la fecha de modificacion
                            actividad.save()
                            add=False

                    if add:

                        a=Actividad(titulo=self.titulo, tipo = self.tipo, precio = self.precio, 
                                    fecha=self.fecha, hora=self.hora, duracion = self.duracion, 
                                    eslargo = self.eslargo, urlinfo = self.urlinfo[12:len(self.urlinfo)], fechamod = fechamod)
                        a.save()

                self.inContent = False
                self.theContent= ""
                inicializar(self)  #inicializa todas las variables

    def characters(self, chars):
        if self.inContent:

            if self.CurrentData == 'CONTENT-URL-ACTIVIDAD':
                self.theContent += chars                #para que escriba la url completa               
            else:
                self.theContent = chars



def getparse(activ, fechmod):

    global actividades, fechamod
    actividades=activ
    fechamod = fechmod

    # Load parser and driver

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    # Ready, set, go!
    theParser.parse("http://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3"+
        "c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&"+
        "format=xml&file=0&filename=206974-0-agenda-eventos-culturales-100&mgmtid="+
        "6c0b6d01df986410VgnVCM2000000c205a0aRCRD")


