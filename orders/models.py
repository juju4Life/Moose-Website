from django.db import models


class GroupName(models.Model):
    added = models.BooleanField(default=False)
    category = models.CharField(max_length=255, default='Unknown')
    group_name = models.CharField(max_length=255, default=None)
    group_id = models.CharField(max_length=255, default=None, unique=True)

    def __str__(self):
        return self.group_name








