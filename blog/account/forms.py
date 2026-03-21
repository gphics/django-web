from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exist")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user
# class RegisterForm(forms.Form):
    # email = forms.EmailField(max_length=30, required=True)
    # username = forms.CharField(max_length=300, required=True)
    # password = forms.CharField(widget=forms.PasswordInput(), max_length=20, min_length=6,error_messages={
    #     "required":"please enter a password",
    #     "min_length":"Password length must be >= 5",
    #     "max_length":"password too long"
    # })
    # confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=20, min_length=6,error_messages={
    #     "required":"please enter a password",
    #     "min_length":"Password length must be >= 5",
    #     "max_length":"password too long"
    # })

    # def clean(self):
    #     cleaned_data = super().clean()

    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")

    #     if password and confirm_password and password != confirm_password:
    #         self.add_error("confirm_password", "The two passwords do not match")
