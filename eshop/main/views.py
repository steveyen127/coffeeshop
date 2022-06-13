from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from . import forms
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guessOrder
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

def registerPage(request):
	form = forms.CreateUserForm()

	if request.method == 'POST':
		form = forms.CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user)
			return redirect('login')

	context = {'form': form}
	return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		if user is not None:
			email = user.email
			customer, created = Customer.objects.get_or_create(
				email = email,
			)
			customer.name = user.username
			customer.user = user
			customer.save()
			login(request, user)
			return redirect('store')
		else:
			messages.info(request, 'Username or Password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def index(request):

	data = cartData(request)
	cartItems = data['cartItems']

	if request.method == 'POST':
		order = request.POST.get('order')
		if order== "Order by name":
			beans = Beans.objects.all().order_by('name')
		elif order== "Order by roast":
			beans = Beans.objects.all().order_by('roast')
		else:
			beans = Beans.objects.all().order_by('flavor_detail')
	else:
		beans = Beans.objects.all()
		# messages.add_message(request, messages.WARNING, "not received")
	return render(request, "shop/index.html", locals())

def cart(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems': cartItems}
	return render(request, 'shop/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems': cartItems}
	return render(request, 'shop/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Beans.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

	else:
		customer, order = guessOrder(request,data)

	total = int(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()
	ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment complete', safe=False)

def bean_detail(request, beanno=0):
	data = cartData(request)
	cartItems = data['cartItems']

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items=[]
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']
	

	if beanno==0:
		return redirect('/')
		
	beans = Beans.objects.get(id=beanno)
	return render(request, "shop/bean_detail.html", locals())

def shop_roast(request, rtype=""):
	if rtype != "":
		selected_beans = Beans.objects.filter(roast=rtype)
	# else:
		# messages.add_message(request, messages.WARNING, "fail")
	return render(request, "shop/shop_roast.html", locals())


def shop_flavor(request, ftype=""):
	if ftype != "":
		selected_beans = Beans.objects.filter(flavor=ftype)
	# else:
	# 	messages.add_message(request, messages.WARNING, "fail")
	return render(request, "shop/shop_flavor.html", locals())


# uses session to send the choosen roast
def roast(request):
	data = cartData(request)
	cartItems = data['cartItems']

	not_last = "/flavor/" #not the last page of the questionnaire 
	if request.method == 'POST':
		form = forms.RoastForm(request.POST)
		if form.is_valid():
			# messages.add_message(request, messages.WARNING, "send roast_form success")
			roast = request.POST['roast']
			selected_beans = Beans.objects.filter(roast=roast)
	else:
		form = forms.RoastForm()

	try:
		# put '#' in session when there's no value in roast, else session==roast
		request.session['roast'] = '#'
		if roast:
			# messages.add_message(request, messages.WARNING, "has roast")
			request.session['roast'] = roast
	except:
		pass
	return render(request, "shop/form.html", locals())


# uses session to send the choosen flavor
def flavor(request):
	data = cartData(request)
	cartItems = data['cartItems']

	roast = request.session['roast']
	not_last = "/flavor_detail/" #not the last page of the questionnaire 
	if request.method == 'POST':
		form = forms.FlavorForm(request.POST)
		if form.is_valid():
			# messages.add_message(request, messages.WARNING, "send roast_form success")
			flavor = request.POST['flavor']
			if roast == '#':
				# there isn't any input from the previous pages
				# messages.add_message(request, messages.WARNING, "no roast")
				selected_beans = Beans.objects.filter(flavor=flavor)
			else:
				# messages.add_message(request, messages.WARNING, "has roast")
				selected_beans = Beans.objects.filter(roast=roast, flavor=flavor)
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


# uses session to send the choosen flavor_detail
def flavor_detail(request):
	data = cartData(request)
	cartItems = data['cartItems']
	
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
				# messages.add_message(request, messages.WARNING, "no roast or flavor")
				if roast=='#' and flavor=='#':
					selected_beans = Beans.objects.filter(flavor_detail=flavor_detail)
				elif roast=='#':
					selected_beans = Beans.objects.filter(flavor=flavor, flavor_detail=flavor_detail)
				else:
					selected_beans = Beans.objects.filter(roast=roast, flavor_detail=flavor_detail)
			else:
				# messages.add_message(request, messages.WARNING, "has roast")
				selected_beans = Beans.objects.filter(roast=roast, flavor=flavor, flavor_detail=flavor_detail)
	else:
		if flavor=='Berry':
			form = forms.FlavorBerryForm()
		elif flavor=='Flower':
			form = forms.FlavorFlowerForm()
		elif flavor=='Wood':
			form = forms.FlavorWoodForm()
		else:
			form = forms.FlavorDetailForm()
		messages.add_message(request, messages.INFO, "Checkbox cannot be empty.")

	try:
		# put '#' in session when there's no value in flavor_detail, else session==flavor_detail
		request.session['flavor_detail'] = '#'
		if flavor:
			request.session['flavor_detail'] = flavor_detail
	except:
		pass
	return render(request, "shop/form.html", locals())







