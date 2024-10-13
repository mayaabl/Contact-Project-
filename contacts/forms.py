from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    # Clean the phone number field (ensure digits only)
    def clean_tel_number(self):
        tel_number = self.cleaned_data.get('tel_number')
        if not tel_number.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        return tel_number

    # Clean the name field to prevent duplicate names only on creation
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Check if this is a new instance (not yet saved)
        if not self.instance.pk and name:  
            # Check for existing name
            if Contact.objects.filter(name=name).exists():
                raise forms.ValidationError('A contact with this name already exists.')
        
        return name
