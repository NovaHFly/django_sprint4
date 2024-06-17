from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """View for 404 page."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request: HttpRequest, reason: str = '') -> HttpResponse:
    """View for 403 page when csrf check fails."""
    return render(request, 'pages/403csrf.html', status=403)
