
from django.db import models

# Create your models here.
class NutritionalInfo(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(blank=True, null=True, max_length=120)
	unit = models.CharField(blank=True, null=True, max_length=120)
	
	def __str__(self):
		return self.name
		
		
class Product(models.Model):
	STATUS = (
       ('active', 'ACTIVE'),
       ('inactive', 'INACTIVE'),
	)
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=160)
	description = models.TextField()
	nutritional_info = models.ManyToManyField(NutritionalInfo, through='NutritionalInfoValues')
	status = models.CharField(
       max_length=32,
       choices=STATUS,
       default='active',
	)
	
	def __str__(self):
		return self.name
		
class NutritionalInfoValues(models.Model):
	nutritional_info = models.ForeignKey(NutritionalInfo, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	values = models.CharField(blank=True, null=True, max_length=120)
	
	def __str__(self):
		return self.values