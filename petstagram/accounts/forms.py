from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from petstagram.accounts.models import Profile
from petstagram.core.forms import BootstrapFormMixin

UserModel = get_user_model()


class LoginForm(AuthenticationForm):
    pass


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email',)


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_image',)
