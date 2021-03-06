from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myreels.models import Order

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class SearchForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)

class OrderForm(forms.Form):
    class Meta:
        model = Order

