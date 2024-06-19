from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    template_name = 'pages/about.html'


class Rules(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """View for 404 page."""
    return render(request, 'pages/404.html', status=404)


def server_failure(request: HttpRequest) -> HttpResponse:
    """View for 500 page."""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request: HttpRequest, reason: str = '') -> HttpResponse:
    """View for 403 page when csrf check fails."""
    return render(request, 'pages/403csrf.html', status=403)
