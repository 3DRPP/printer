from django.contrib.auth import logout, authenticate, login
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _


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