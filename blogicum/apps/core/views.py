from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect
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
