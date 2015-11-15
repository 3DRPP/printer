from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from printer.models import Printable, User
from printer import gpio
from printer import settings

def home(request):
    return render(
        request,
        'base.html'
    )

def my_login(request):
    if request.user.is_authenticated():
        raise Http404()

    error = None
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        stay_connected = request.POST.get('stay_connected', False)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if stay_connected != False:
                # Session will expires in 30 days
                request.session.set_expiry(2592000)
            return HttpResponseRedirect(reverse('printer.views.home'))
        else:
            error = _("Nom d'utilisateur ou mot de passe incorrect.")
    context = {
        'error': error
    }
    return render_to_response(
        'login.html',
        context,
        context_instance=RequestContext(request)
    )

@login_required
def tasks(request):
    if request.user.is_admin:
        waiting_tasks = Printable.objects.filter(date_start=None).order_by('-date_added').all()
    else:
        waiting_tasks = Printable.objects.filter(date_start=None, owner=request.user).order_by('-date_added').all()
    context = {
        'waiting_tasks' : waiting_tasks
    }
    return render(
        request,
        'tasks.html',
        context
    )

@login_required
def add_task(request):

    error = None
    if request.POST and request.FILES:
        name = request.POST.get('name')
        filename = request.POST.get('filename')
        comment = request.POST.get('comment')

        if name == '' or filename == '' or comment == '':
            raise Http404('Invalid input')

        try:
            Printable.objects.get(name=name)
            raise Http404('Ce nom existe déjà.')
        except:
            pass


        file = request.FILES['file']
        djangofile = File(file)

        task = Printable()
        task.name = name
        task.comment = comment
        task.owner = request.user
        task.file.save(filename, djangofile)
        task.filename = filename
        task.save()

        djangofile.close()

        #TODO: check the file format & file validity (size...)
        return HttpResponse()

    context = {
        'error': error
    }
    return render_to_response(
        'login.html',
        context,
        context_instance=RequestContext(request)
    )

@login_required
def admin(request, error=None):
    if not request.user.is_admin:
        raise Http404()

    context = {
        'error': error,
        'users': User.objects.all(),
        'gpio_header' : gpio.header
    }
    return render(
        request,
        'admin.html',
        context
    )

@login_required
def add_user(request):
    if not request.user.is_admin:
        raise Http404()

    error = None
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('pass')
        type = int(request.POST.get('type'))
        if name == '' or email == '' or first_name == '' or last_name == '' or \
            password == '' or type == '':
            error = 'Veuillez remplir tous les champs.'
        else:
            try:
                u = User()
                u.name = name
                u.email = email
                u.first_name = first_name
                u.last_name = last_name
                u.set_password(password)
                if type == 1:
                    u.is_admin = True
                u.save()
            except:
                error = 'Champs invalides.'

    return admin(request, error)

@login_required
def del_user(request):
    if not request.user.is_admin:
        raise Http404()

    if request.GET:
        user_id = request.GET.get('user_id')
        try:
            u = User.objects.get(id=user_id)
        except:
            raise Http404()
        if u == request.user:
            raise Http404()
        u.delete()

    return admin(request)



@login_required
def gpio_switch(request):
    if not request.user.is_admin:
        raise Http404()

    if request.GET:
        gpio_id = int(request.GET.get('gpio_id'))
        if not gpio_id in gpio.gpios:
            raise Http404()
        gpio.header.switch_value(gpio_id)
        return HttpResponse()
    raise Http404()


@login_required
def gpio_switch_mode(request):
    if not request.user.is_admin:
        raise Http404()

    if request.GET:
        gpio_id = int(request.GET.get('gpio_id'))
        if not gpio_id in gpio.gpios:
            raise Http404()
        mode, value = gpio.header.switch_mode(gpio_id)
        return HttpResponse(value)
    raise Http404()




def my_400(request):
    #TODO
    context = {
        'number': '404',
        'short_description': _("Une erreur est survenue"),
        'full_description': _("L'URL demandée n'a pas abouti. Peut-être vous "
                              "êtes vous trompé d'adresse ?")
    }
    return render(
        request,
        'x0x.html',
        context
    )

def my_403(request):
    #TODO
    context = {
        'number': '404',
        'short_description': _("Une erreur est survenue"),
        'full_description': _("L'URL demandée n'a pas abouti. Peut-être vous "
                              "êtes vous trompé d'adresse ?")
    }
    return render(
        request,
        'x0x.html',
        context
    )

def my_404(request):
    context = {
        'number': '404',
        'short_description': _("Une erreur est survenue"),
        'full_description': _("L'URL demandée n'a pas abouti. Peut-être vous "
                              "êtes vous trompé d'adresse ?")
    }
    return render(
        request,
        'x0x.html',
        context
    )

def my_500(request):
    #TODO
    context = {
        'number': '404',
        'short_description': _("Une erreur est survenue"),
        'full_description': _("L'URL demandée n'a pas abouti. Peut-être vous "
                              "êtes vous trompé d'adresse ?")
    }
    return render(
        request,
        'x0x.html',
        context
    )

def live_stream(request):
    if not settings.live_stream['activated']:
        return
    context = {
        'livestream_url': settings.live_stream['url']
    }
    return render_to_response(
        'live.html',
        context,
        context_instance=RequestContext(request)
    )