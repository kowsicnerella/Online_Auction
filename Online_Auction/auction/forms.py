from captcha.fields import CaptchaField
from django import forms


class LoginForm(forms.Form):

    captcha = CaptchaField()
