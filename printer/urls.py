from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from printer.settings import SITE_URL_PREFIX, SITE_URL, STATIC_URL, STATICFILES_DIRS
from printer.views import home, my_login, my_400, my_403, my_404, my_500
from django.contrib.auth.views import logout
from django.conf.urls import handler400, handler403, handler404, handler500

base_urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^connexion/$', my_login, name='login'),
    url(r'^deconnexion/$', logout, {'next_page': 'printer.views.home'}, name='logout'),
)

urlpatterns = patterns(
    '',
    url(r'^' + SITE_URL_PREFIX, include(base_urlpatterns))
)
# ) + static(STATIC_URL, document_root=STATICFILES_DIRS)


handler400 = my_400
handler403 = my_403
handler404 = my_404
handler500 = my_500