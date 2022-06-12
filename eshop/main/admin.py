from django.contrib import admin
from main import models

class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('order','product', 'quantity', 'date_added')

class OrderAdmin(admin.ModelAdmin):
	list_display = ('id','customer','complete')

class BeansAdmin(admin.ModelAdmin):
	list_display = ('name','roast','flavor')

class AddressAdmin(admin.ModelAdmin):
	list_display = ('order','customer','address')

admin.site.register(models.Beans, BeansAdmin)
admin.site.register(models.Customer)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.ShippingAddress, AddressAdmin)