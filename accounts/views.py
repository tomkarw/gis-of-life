from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
