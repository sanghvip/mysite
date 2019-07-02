from django import forms
from django.db import models
from myapp.models import *
from django.contrib.auth.forms import UserCreationForm

#Create your forms here

#OrderForm for order placement
class OrderForm(forms.ModelForm):

    class Meta:
        model=Order
        fields = ['client', 'product', 'num_units']

    client = forms.ModelChoiceField(queryset=Client.objects.all(), label='Client Name')
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    num_units = forms.IntegerField(label='Quantity')

#InterestedForm for products interests
class InterestForm(forms.Form):
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=[(1,'Interested'),(0,'Not interested')], label='Interested')
    quantity = forms.IntegerField(initial=1, label='Quantity')
    comments = forms.CharField(widget=forms.Textarea, required=False, label='Additional Comments')

#SignupForm to add custom fields in sign up page
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Client
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )