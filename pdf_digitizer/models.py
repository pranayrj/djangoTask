import random
import string

from django.db import models
from django.urls import reverse

def upload_location(instance,filename):
    return f"documents/{instance.invoiceid}/{filename}"

class InvoiceFileUpload(models.Model):
    document = models.FileField(upload_to=upload_location)
    uploaded_time = models.DateTimeField(auto_now_add=True)
    invoiceid = models.CharField(max_length=200, blank=True, primary_key=True)

    def id_generator(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    # Can also write signals to implement the same functionality of creating new instance of structureddata for every
    # upload But Save works by calling signals and is easier to read and also once the project gets bigger its tough
    # to track signals.
    def save(self, *args, **kwargs):
        self.invoiceid = self.id_generator()

        InvoiceStructuredData.objects.create(invoiceid=self.invoiceid)
        super(InvoiceFileUpload, self).save(*args, **kwargs)


class InvoiceStructuredData(models.Model):
    """Activity Period model to contain time logs of when they are active,
     their respective starting and ending time"""

    invoiceid = models.CharField(max_length=200, blank=True, primary_key=True)
    invoice_number = models.CharField(max_length=200, blank=True, null=True)
    date_of_purchase = models.CharField(max_length=200, blank=True, null=True)
    vendor_name = models.CharField(max_length=200, blank=True, null=True)
    purchaser_name = models.CharField(max_length=200, blank=True, null=True)
    purchaser_contact = models.CharField(max_length=200, blank=True, null=True)
    vendor_address = models.TextField(null=True, blank=True)
    purchase_amount = models.CharField(max_length=100, null=True, blank=True)
    items_purchased = models.TextField(null=True, blank=True)
    digitized = models.BooleanField(default=False, blank=True)
    updated_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoiceid}"