from django.shortcuts import render
from main import models
from django.contrib import messages
from . import forms

def index(request):
	beans = models.Beans.objects.all()
	return render(request, "shop/index.html", locals())

def roast(request):
	not_last = "/flavor/" #not the last page of the questionnaire 
	if request.method == 'POST':
		form = forms.RoastForm(request.POST)
		if form.is_valid():
			# messages.add_message(request, messages.WARNING, "send roast_form success")
			roast = request.POST['roast']
			selected_beans = models.Beans.objects.filter(roast=roast)
	else:
		form = forms.RoastForm()

	try:
		# put '#' in session when there's no value in roast, else session==roast
		request.session['roast'] = '#'
		if roast:
			messages.add_message(request, messages.WARNING, "has roast")
			request.session['roast'] = roast
	except:
		pass
	return render(request, "shop/form.html", locals())


def flavor(request):
	not_last = "/flavor_detail/" #not the last page of the questionnaire 
	if request.method == 'POST':
		form = forms.FlavorForm(request.POST)
		if form.is_valid():
			# messages.add_message(request, messages.WARNING, "send roast_form success")
			flavor = request.POST['flavor']
			roast = request.session['roast']
			if roast == '#':
				# there isn't any input from the previous pages
				messages.add_message(request, messages.WARNING, "no roast")
				selected_beans = models.Beans.objects.filter(flavor=flavor)
			else:
				messages.add_message(request, messages.WARNING, "has roast")
				selected_beans = models.Beans.objects.filter(roast=roast, flavor=flavor)
	else:
		form = forms.FlavorForm()

	try:
		# put '#' in session when there's no value in flavor, else session==flavor
		request.session['flavor'] = '#'
		if flavor:
			request.session['flavor'] = flavor
	except:
		pass
	return render(request, "shop/form.html", locals())


def flavor_detail(request):
	not_last = "" #the last page of the questionnaire 
	roast = request.session['roast']
	flavor = request.session['flavor']
	if request.method == 'POST':
		if flavor=='Berry':
			form = forms.FlavorBerryForm(request.POST)
		elif flavor=='Flower':
			form = forms.FlavorFlowerForm(request.POST)
		elif flavor=='Wood':
			form = forms.FlavorWoodForm(request.POST)
		else:
			form = forms.FlavorDetailForm(request.POST)

		if form.is_valid():
			# messages.add_message(request, messages.WARNING, "send roast_form success")
			roast = request.session['roast']
			flavor = request.session['flavor']
			flavor_detail = request.POST['flavor_detail']
			if roast == '#' or flavor=='#':
				# there isn't any input from the previous pages
				messages.add_message(request, messages.WARNING, "no roast or flavor")
				if roast=='#' and flavor=='#':
					selected_beans = models.Beans.objects.filter(flavor_detail=flavor_detail)
				elif roast=='#':
					selected_beans = models.Beans.objects.filter(flavor=flavor, flavor_detail=flavor_detail)
				else:
					selected_beans = models.Beans.objects.filter(roast=roast)
			else:
				messages.add_message(request, messages.WARNING, "has roast")
				selected_beans = models.Beans.objects.filter(roast=roast, flavor=flavor, flavor_detail=flavor_detail)
	else:
		if flavor=='Berry':
			form = forms.FlavorBerryForm()
		elif flavor=='Flower':
			form = forms.FlavorFlowerForm()
		elif flavor=='Wood':
			form = forms.FlavorWoodForm()
		else:
			form = forms.FlavorDetailForm()

	try:
		# put '#' in session when there's no value in flavor, else session==flavor
		request.session['flavor_detail'] = '#'
		if flavor:
			request.session['flavor_detail'] = flavor_detail
	except:
		pass
	return render(request, "shop/form.html", locals())






