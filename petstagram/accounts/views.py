from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from petstagram.accounts.forms import LoginForm, RegisterForm, ProfileForm
from petstagram.accounts.models import Profile
from petstagram.pets.models import Pet


UserModel = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('landing page')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm


class ProfileFormView(LoginRequiredMixin, FormView):
    form_class = ProfileForm
    template_name = 'accounts/user_profile.html'
    success_url = reverse_lazy('profile details')

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)

        result['pets'] = Pet.objects.filter(user_id=self.request.user.id)
        result['profile'] = Profile.objects.get(pk=self.request.user.id)

        return result

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.request.user.id)
        profile.profile_image = form.cleaned_data['profile_image']
        profile.save()
        return super().form_valid(form)


def logout_user(request):
    logout(request)
    return redirect('landing page')
