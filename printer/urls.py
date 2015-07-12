from django.conf.urls import patterns, include, url
from printer.settings import SITE_URL_PREFIX
from printer.views import home, my_login, admin, gpio_switch, tasks, add_task,\
    my_400, my_403, my_404, my_500, add_user, del_user
from django.contrib.auth.views import logout

base_urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^taches/$', tasks, name='tasks'),
    url(r'^taches/add/$', add_task, name='add_task'),
    url(r'^admin/switch_gpio/', gpio_switch, name='gpio_switch'),
    url(r'^admin/add_user/', add_user, name='add_user'),
    url(r'^admin/del_user/', del_user, name='del_user'),
    url(r'^admin/', admin, name='admin'),
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