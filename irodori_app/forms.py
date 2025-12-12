from django import forms
from .models import Customer,Activity

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer

        fields = ('company_name', 'contact_name', 'email', 'phone', 'user', 'tags')


        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity

        fields = ('activity_date', 'status', 'note')


        widgets = {
            'activity_date': forms.DateInput (attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control','rows':2 }),
        }