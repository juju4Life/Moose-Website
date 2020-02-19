from django.db import models


class CustomerEmail(models.Model):
    email_address = models.EmailField()
    name = models.CharField(max_length=30, default='')
    order_number = models.CharField(max_length=15, default='', blank=True)
    message = models.TextField()
    reply = models.TextField(blank=True)
    subject = models.CharField(max_length=50, default='')
    message_created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.CharField(max_length=25, default='', blank=True)
    uuid = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.email_address


