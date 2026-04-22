from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from shop.models import Category,Product

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username','email','password1','password2','first_name','last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = None


class LoginForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields ='__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields ='__all__'

class StockForm(forms.ModelForm):
    class Meta:
        model =Product
        fields = ['stock']


