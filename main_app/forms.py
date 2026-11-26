from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Booking, ContactMessage, UserProfile


class RegisterForm(forms.Form):
    INTENT_DETAIL_LABELS = {
        'learning': 'What would you like to learn?',
        'studio': 'What session are you planning?',
        'event': 'What event are you planning?',
        'other': 'Tell us a little more (optional)',
    }

    intent = forms.ChoiceField(choices=UserProfile.INTENT_CHOICES, initial='learning')
    intent_detail = forms.CharField(max_length=255, required=False, widget=forms.TextInput)
    full_name = forms.CharField(max_length=120)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    agree_terms = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['intent'].required = False
        self.fields['agree_terms'].error_messages = {
            'required': 'You must agree to the Terms and Privacy Policy to continue.'
        }

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm = cleaned.get('confirm_password')
        if password and confirm and password != confirm:
            self.add_error('confirm_password', 'Passwords do not match.')
        if password:
            try:
                validate_password(password)
            except forms.ValidationError as e:
                self.add_error('password', e)
        return cleaned


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address', 'autocomplete': 'email'})
    )


class SetNewPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm = cleaned.get('confirm_password')
        if password and confirm and password != confirm:
            self.add_error('confirm_password', 'Passwords do not match.')
        if password:
            try:
                validate_password(password)
            except forms.ValidationError as e:
                self.add_error('password', e)
        return cleaned


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


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}),
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'How can we help?'}),
            'message': forms.Textarea(attrs={'class': 'form-input h-40', 'placeholder': 'Tell us about your project or question...'}),
        }
