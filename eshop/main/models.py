from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Beans(models.Model):
	ROAST = (
		('Light', 'Light'),
		('Medium', 'Medium'),
		('Dark', 'Dark'),
	)
	name = models.CharField(max_length=200, null=True)
	price = models.PositiveIntegerField(default=0, null=False)
	picture = models.URLField()
	description = models.TextField()
	origin = models.CharField(max_length=100, null=False)
	roast = models.CharField(max_length=50, choices=ROAST)
	flavor = models.CharField(max_length=100, null=True)
	flavor_detail = models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.name

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=False)
	transaction_id = models.CharField(max_length=200, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

class OrderItem(models.Model):
	product = models.ForeignKey(Beans, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
	

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address

# class FlavorDetail(models.Model):
# 	beans = models.ManyToManyField(Beans)
# 	flavor = models.CharField(max_length=100, null=True)
# 	# detail = models.CharField(max_length=100, null=True)
# 	def __str__(self):
# 		return self.flavor

