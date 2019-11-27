from django import forms

from .models import Visit, Provider

class VisitForm(forms.ModelForm):

    class Meta:
        model = Visit
        fields = ('provider', 'floor',)

class NewProvider(forms.ModelForm):

	class Meta:
		model = Provider
		fields = ['name', 'shortcut', 'logo']
		labels = {'name': 'Nazwa:', 
				'shortcut': 'Skrót:',
				'logo': 'Logo:'}