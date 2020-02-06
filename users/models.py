from django.db import models


class State(models.Model):
    name = models.CharField(max_length=255, default='')
    abbreviation = models.CharField(max_length=2, default='')

    def __str__(self):
        return self.name










