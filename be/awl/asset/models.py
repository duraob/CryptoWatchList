from django.db import models

# Create your models here.
class Asset(models.Model):
    coin_id = models.CharField(max_length=50)
    symbol = models.CharField(max_length=75)
    quote = models.FloatField()
    mrkt_cap = models.FloatField()
    vol = models.FloatField()
    change_day = models.FloatField()
    change_week = models.FloatField()
    change_month = models.FloatField()

    def __str__(self):
        return self.symbol