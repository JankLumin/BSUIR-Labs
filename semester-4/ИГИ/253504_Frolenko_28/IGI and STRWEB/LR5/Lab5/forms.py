from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        help_text='Required. Format: YYYY-MM-DD',
        widget=DateInput(attrs={'type': 'date', 'min': '1900-01-01', 'required': 'required'})
    )

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('role', 'birth_date')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['role'].required = True
        self.fields['birth_date'].required = True

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise ValidationError("You must be at least 18 years old to register.")
        return birth_date
