from django.db import models

class Beans(models.Model):
	ROAST = (
		('Light', 'Light'),
		('Medium', 'Medium'),
		('Dark', 'Dark'),
	)
	name = models.CharField(max_length=100, null=False)
	price = models.PositiveIntegerField(default=0, null=False)
	picture = models.URLField()
	description = models.TextField()
	origin = models.CharField(max_length=100, null=False)
	roast = models.CharField(max_length=50, choices=ROAST)
	flavor = models.CharField(max_length=100, null=True)
	flavor_detail = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.name

# class FlavorDetail(models.Model):
# 	beans = models.ManyToManyField(Beans)
# 	flavor = models.CharField(max_length=100, null=True)
# 	# detail = models.CharField(max_length=100, null=True)
# 	def __str__(self):
# 		return self.flavor
