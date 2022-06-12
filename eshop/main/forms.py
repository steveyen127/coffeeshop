# _*_encoding:utf-8 *_*
from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit

FLAVOR_CHOICES = (
	('Flower', 'Flower'),
	('Berry', 'Berry'),
	('Wood', 'Wood'),
)

FLAVOR_DETAIL_CHOICES = (
	('Blueberry', 'Blueberry'),
	('Strawberry', 'Strawberry'),
	('Raspberry', 'Raspberry'),
	('Cherry', 'Cherry'),
	('Rose', 'Rose'),
	('Sunflower', 'Sunflower'),
	('Vanilla', 'Vanilla'),
	('Pine', 'Pine'),
	('Sandalwood', 'Sandalwood'),
	('Dark Chocolate', 'Dark Chocolate'),
)

FLAVOR_BERRY_CHOICES = (
	('Blueberry', 'Blueberry'),
	('Strawberry', 'Strawberry'),
	('Raspberry', 'Raspberry'),
	('Cherry', 'Cherry'),
)

FLAVOR_FLOWER_CHOICES = (
	('Rose', 'Rose'),
	('Sunflower', 'Sunflower'),
	('Vanilla', 'Vanilla'),
)

FLAVOR_WOOD_CHOICES = (
	('Pine', 'Pine'),
	('Sandalwood', 'Sandalwood'),
	('Dark Chocolate', 'Dark Chocolate'),
)

ROAST_CHOICES = (
	('Light', 'Light'),
	('Medium', 'Medium'),
	('Dark', 'Dark'),
)

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class RoastForm(forms.Form):
	roast = forms.ChoiceField(widget=forms.RadioSelect, label="Roast", choices=ROAST_CHOICES)
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.helper = FormHelper()
	# 	self.helper.roast = 'Roast'
		# self.helper.add_input(Submit('submit', 'submit'))

class FlavorForm(forms.Form):
	flavor = forms.ChoiceField(widget=forms.RadioSelect, label="Flavor", choices=FLAVOR_CHOICES)
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.helper = FormHelper()
	# 	self.helper.flavor = 'Flavor'

class FlavorDetailForm(forms.Form):
	flavor_detail = forms.ChoiceField(widget=forms.RadioSelect, label="Flavor Detail", choices=FLAVOR_DETAIL_CHOICES)

class FlavorBerryForm(forms.Form):
	flavor_detail = forms.ChoiceField(widget=forms.RadioSelect, label="Flavor Detail", choices=FLAVOR_BERRY_CHOICES)

class FlavorFlowerForm(forms.Form):
	flavor_detail = forms.ChoiceField(widget=forms.RadioSelect, label="Flavor Detail", choices=FLAVOR_FLOWER_CHOICES)

class FlavorWoodForm(forms.Form):
	flavor_detail = forms.ChoiceField(widget=forms.RadioSelect, label="Flavor Detail", choices=FLAVOR_WOOD_CHOICES)


# class PreferenceForm(forms.Form):
	# class Meta:
	# 	model = models.FlavorDetail
	# 	fields = ['detail']
	# flavor = forms.ModelMultipleChoiceField(queryset=models.FlavorDetail.objects.all(), widget=forms.CheckboxSelectMultiple(), label="Preference", choices=CHOICES)
	# flavor = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), label="Preference", choices=FLAVOR_CHOICES)

	# def __init__(self, *args, **kwargs):
	# 	super(PreferenceForm, self).__init__(*args, **kwargs)
		# self.fields['flavor'].queryset = models.FlavorDetail.objects.all()

		# super(PreferenceForm, self).__init__(*args, **kwargs)
		# self.fields['beans'].label = 'Bean Name'
		# self.fields['flavor'].label = 'Flavor'
		# self.fields['detail'].label = 'Category'

