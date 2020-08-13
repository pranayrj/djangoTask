import json

from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.views.generic.base import View
from .models import InvoiceStructuredData
from .forms import DocumentForm
from django.shortcuts import get_object_or_404


# @csrf_exempt
# def model_form_upload(request):
#     if request.method == 'POST':
#         print(request.FILES)
#         form = DocumentForm(request.POST, request.FILES)
#         print(form.is_valid())
#         if form.is_valid():
#             form.save()
#             return JsonResponse({"r()":"zx"}, safe=False)
#
#     return JsonResponse({"render()":"zx"}, safe=False)

@method_decorator(csrf_exempt, name='dispatch')  # since form is not used and hence csrf token not includede there so
# expecting the outermost view fn dispatch
class FormUpload(View):

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({"message":"file uploaded",'status': 'success','code': 200}, safe=False)


class DigitizationStatus(View):

    def check_if_digitized(self, invoiceid):
        try:
            check_object = get_object_or_404(InvoiceStructuredData, invoiceid=invoiceid)
            if check_object.digitized:
                return check_object
            return False
        except:
            is_digitized = "Object Not Found"
            return is_digitized

    def get(self, request, *args, **kwargs):
        digitized_object = self.check_if_digitized(kwargs['invoiceid'])
        if digitized_object == "Object Not Found":
            return JsonResponse({"message":"Wrong InvoiceID",'status': 'success','code': 200}, safe=False)

        elif digitized_object:
            return JsonResponse({"message":"Digitized, please proceed to check digitized data",'status': 'success','code': 200}, safe=False)
        else:
            return JsonResponse({"message":"Not yet digitized",'status': 'success','code': 200}, safe=False)

        # try:
        #     if digitized_object.digitized:
        #         return HttpResponse("Digitized, please proceed to check digitized data")
        #     else:
        #         return HttpResponse("Not yet digitized")
        # except:
        #     return HttpResponse("Document is not digitized or wrong Invoice Number.")


class RetrieveStructuredData(DigitizationStatus):

    def get(self, request, *args, **kwargs):
        digitized_object = self.check_if_digitized(kwargs['invoiceid'])
        if digitized_object == "Object Not Found":
            return JsonResponse({"message":"Wrong InvoiceID",'status': 'success','code': 200}, safe=False)
        elif digitized_object:
            dummy_data={"invoice_number":"XZC123","purchase_date":"20/08/2020"}
            return JsonResponse({"dummy_data":dummy_data,'status': 'success','code': 200}, safe=False)
        else:
            return JsonResponse({"message":"Not yet digitized",'status': 'success','code': 200}, safe=False)

        # try:
        #     if digitized_object.digitized:
        #         return HttpResponse(digitized_object.date_of_purchase)
        #     else:
        #         return HttpResponse("Not yet digitized")
        # except:
        #     return HttpResponse("Document is not digitized(Invoice Number not yet registered) or wrong Invoice Number.")


## so here we can write 2 views for /digitization_status/invoicenumber and /invoicenumber
# /invoicenumber check for object , if present ok... then check for digitization status= true or false give msg accordingly.
# if not present tell them wrong invoice number.
#
# we can inherit one class based view from another so that db querying is not done again and again.


# from django.contrib.admin.views.decorators import staff_member_required
# from django.utils.decorators import method_decorator
#
# If User authentication is activated then we can limit the apis to staff members only and not to end users
# @method_decorator(staff_member_required, name='dispatch')

@method_decorator(csrf_exempt, name='dispatch')
class AddStructuredData(View):
    model = InvoiceStructuredData

    def post(self, request, *args, **kwargs):
        received_json_data = {}

        try:
            data = request.body.decode('utf-8')
            received_json_data = json.loads(data)
        except Exception:
            print(Exception)
        invoice = InvoiceStructuredData.objects.get(invoiceid=kwargs['invoiceid'])

        for key, value in received_json_data.items():
            setattr(invoice, key, value)

        invoice.save(update_fields=received_json_data.keys())
        return JsonResponse({"message": "Data Added Succesfully", 'status': 'success', 'code': 200}, safe=False)
