import datetime

from django.db import models


class Energy(models.Model):
    active_energy = models.DecimalField(max_digits=10, decimal_places=2)
    meter_date = models.DateTimeField()

    def __str__(self):
        return str(self.active_energy)
