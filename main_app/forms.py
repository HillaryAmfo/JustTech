from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'company', 'service', 'preferred_date', 'preferred_time', 'notes']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'preferred_time': forms.Select(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'company': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Company (optional)'}),
            'notes': forms.Textarea(attrs={'class': 'form-input h-32', 'placeholder': 'Tell us about your project or specific requirements...'}),
            'service': forms.Select(attrs={'class': 'form-input'}),
        }
