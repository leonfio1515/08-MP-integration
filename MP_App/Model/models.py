from django.db import models
from django.contrib.auth.models import User
#----------------------------------------------------#

class Articulo(models.Model):
    cod_art = models.CharField(max_length=50)
    name_art = models.CharField(max_length=50)
    price_art = models.FloatField()
    stock_art = models.PositiveIntegerField()


class Cliente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

class Compras(models.Model):
    art = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)
    tot_amount = models.PositiveIntegerField(default=0)