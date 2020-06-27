from django import forms
from django.forms import ModelForm
from django.forms import formset_factory, inlineformset_factory
from restaurant.models import Product, NutritionalInfoValues, NutritionalInfo

class MyFormSimple(forms.Form):
	STATUS = (
       ('active', 'ACTIVE'),
       ('inactive', 'INACTIVE'),
	)
	nombre = forms.CharField(label='Nombre:',max_length=160)
	description = forms.CharField(label='Description:')
	status = forms.ChoiceField(label='Status:',
       choices=STATUS,
	)

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ["name", "description", "status"]

		
class NutritionalInfoValuesForm(ModelForm):
	class Meta:
		model = NutritionalInfoValues
		fields = ["nutritional_info","values"]

NutritionalInfoValuesFormFormSet = formset_factory(NutritionalInfoValuesForm, extra=4, max_num=4)