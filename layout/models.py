from django.db import models
from cloudinary.models import CloudinaryField


class CompanyAddress(models.Model):
    company = models.CharField(max_length=255, default='')
    address_line_1 = models.CharField(max_length=255, default='')
    address_line_2 = models.CharField(max_length=255, default='', blank=True)
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    zip_code = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.address_line_1

    class Meta:
        verbose_name_plural = 'Company Address'


class DocumentTemplate(models.Model):
    title = models.CharField(max_length=255, default='')
    overview = models.TextField(default='')
    effective_date = models.DateField(blank=True, auto_now=True)

    class Meta:
        abstract = True


class DocumentBlock(models.Model):
    header = models.CharField(max_length=255, default='')
    paragraph = models.TextField(default='')

    class Meta:
        abstract = True


class HomePageLayout(models.Model):
    name = models.CharField(max_length=255, default='')
    image = CloudinaryField('image')
    text = models.TextField(blank=True)

    def __str__(self):
        return self.name


class PreorderItem(models.Model):
    image = CloudinaryField('image')
    expansion = models.OneToOneField('orders.GroupName', on_delete=models.CASCADE)

    def __str__(self):
        return self.expansion.group_name


class PrivacyPolicy(DocumentTemplate):
    reserved_right_clause = models.TextField(default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Privacy Policy'


class PrivacyPolicyBlock(DocumentBlock):

    def __str__(self):
        return self.header


class SinglePrintingSet(models.Model):
    expansion = models.CharField(max_length=255, default='')
    normal_only = models.BooleanField(default=False)
    foil_only = models.BooleanField(default=False)

    def __str__(self):
        return self.expansion


class TermsOfService(DocumentTemplate):
    def __str__(self):
        return self.title


class TermsOfServiceBlock(DocumentBlock):
    def __str__(self):
        return self.header


class Text(models.Model):
    category = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    clean_name = models.CharField(max_length=255, default='')
    text = models.TextField(default='')

    def __str__(self):
        return self.name



