from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import Profile

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class UserFormUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileFormUpdate(forms.ModelForm):
    date_birth = forms.DateField(widget=forms.DateInput)

    class Meta:
        model = Profile
        fields = ['date_birth', 'photo', 'location']
