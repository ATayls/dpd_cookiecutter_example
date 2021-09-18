from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from allauth.account import forms as auth_forms
from django_countries.fields import CountryField
from django import forms

from dpd_cc_example.data.models import Team

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
        error_messages = {
            "username": {"unique": _("This email has already been taken.")}
        }


class MyCustomSignupForm(auth_forms.SignupForm):

    country = CountryField(blank_label='(Select country)').formfield()
    favourite_team = forms.ModelChoiceField(queryset=Team.objects.all())

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)

        self.fields["password2"].label = "Password Confirmation"

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user
