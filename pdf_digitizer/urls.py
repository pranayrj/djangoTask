from django.urls import path

from pdf_digitizer import views

app_name="pdf_digitizer"

# URl .using invoice_number as slug, considering invoices are of same company and are hence unique
urlpatterns = [
    path("upload/", views.FormUpload.as_view(),name="form_upload"),
    path('digitized/<str:invoiceid>/', views.DigitizationStatus.as_view(),name="is_digitized"),
    path('<str:invoiceid>/', views.RetrieveStructuredData.as_view(),name="detail"),
    path('<str:invoiceid>/add_data', views.AddStructuredData.as_view(),name="invoice_data"),
]
