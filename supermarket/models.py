from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=1, unique=True)
    unit_price = models.PositiveIntegerField()
    discount_quantity = models.PositiveIntegerField(null=True, blank=True)
    discount_price = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
