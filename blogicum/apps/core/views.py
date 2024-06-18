from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView


class Registration(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form: UserCreationForm) -> HttpResponse:
        """If the form is valid, save the associated model."""
        user = form.save()
        login(self.request, user)

        return redirect(self.success_url)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """View for 404 page."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request: HttpRequest, reason: str = '') -> HttpResponse:
    """View for 403 page when csrf check fails."""
    return render(request, 'pages/403csrf.html', status=403)
