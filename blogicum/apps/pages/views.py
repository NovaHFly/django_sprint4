from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def about(request: HttpRequest) -> HttpResponse:
    """Show page with info about the project.

    Args:
        request (HttpRequest): Request received from the user.
    """
    template = 'pages/about.html'
    return render(request, template)


def rules(request: HttpRequest) -> HttpResponse:
    """Show page with rules.

    Args:
        request (HttpRequest): Request received from the user.
    """
    template = 'pages/rules.html'
    return render(request, template)
