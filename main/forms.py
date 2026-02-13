# main/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Package
from .models import Booking
from django.utils import timezone

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email or username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['title', 'subtitle', 'price', 'slug', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'travel_date', 'persons']

    def clean_travel_date(self):
        travel_date = self.cleaned_data['travel_date']

        if travel_date < timezone.now().date():
            raise forms.ValidationError("Travel date cannot be in the past.")

        return travel_date