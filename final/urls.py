from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'final.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ingresar$','apps.views.ingresar'),
    url(r'^apariencia$','apps.views.formato'),
    url(r'^cleancss$','apps.views.cleancss'),
    url(r'^logout$', "apps.views.salir"),
    url(r'^rss$', "apps.views.rsshome"),
    url(r'^puntuacion/(.+)', "apps.views.puntuacion"),
    url(r'^comentario/(.+)', "apps.views.putcomment"),    


   
    url(r'^update', 'apps.views.getactividades'),
    url(r'^clean', 'apps.views.cleanall'), #vacia actividades
    url(r'^(.*)/rss$', 'apps.views.createrss'),
    url(r'^addactividad/(.*)', 'apps.views.addactividad'),
    url(r'^delactividad/(.*)', 'apps.views.delactividad'),


    
	#url(r'^/css/(?P<path>.*)$', 'django.views.static.serve', 
#{'document_root': settings.STATIC_URL2}),
    # url(r'^$', 'apps.views.showhome'),





    url(r'^(.*)css/(?P<path>.*)$','django.views.static.serve',
{'document_root': settings.STATIC_URL2}),

    url(r'^todas', 'apps.views.showall'),
    url(r'^actividad/(.*)','apps.views.showactividad'),
    url(r'^ayuda', 'apps.views.ayudas'),
   
    url(r'^(.*)/(.*)','apps.views.usuario'),
    url(r'^$','apps.views.showhome'),
 


 	
    
    

)
