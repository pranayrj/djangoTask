from django.contrib import admin

# Register your models here.
from .models import InvoiceFileUpload,InvoiceStructuredData

admin.site.register(InvoiceFileUpload)
admin.site.register(InvoiceStructuredData)
