from printer import settings
import socket
from django.contrib.sites.shortcuts import get_current_site


def site_infos(request):
    current_site = get_current_site(request)
    protocol = 'https'  # if request.is_secure() else 'http'
    domain = current_site.domain

    return {
        'protocol': protocol,
        'domain': domain,
        'hostname': socket.gethostname(),
        'livestream_activated': settings.live_stream['activated']
    }