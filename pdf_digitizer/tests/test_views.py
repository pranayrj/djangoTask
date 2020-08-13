import json

from django.test import TestCase, Client
from ..models import InvoiceStructuredData,InvoiceFileUpload
from .test_models import ModelsTestCase

class ViewsTestCase(TestCase):
    test_invoice_id="Randomid"
    def test_upload_api_loads_properly(self):
        """Test to check the availability of the API"""

        # checking Response code by asserting it to 200
        c = Client()
        with open('requirements.txt') as fp:
            response= c.post('/upload/', {'document': fp})
        self.assertEqual(response.status_code, 200)

    def test_digitization_and_retrieve_data_api(self):
        """Test to check the availability of the API"""

        # checking Response code by asserting it to 200
        object=ModelsTestCase.test_model_can_create_invoice_model(self)

        response = self.client.get(f'/digitized/{object.invoiceid}/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/{object.invoiceid}/')
        self.assertEqual(response.status_code, 200)


    def test_update_data_api(self):
        """Test to check the availability of the API"""
        object = ModelsTestCase.test_model_can_create_invoice_model(self)

        # checking Response code by asserting it to 200
        # json_data=json.loads()
        response = self.client.post(f'/{object.invoiceid}/add_data',{"invoice_number":"something else"})
        self.assertEqual(response.status_code, 200)



    # def test_fields_in_json_response(self):
    #     """Test to check fields present in the Json response"""
    #
    #     # Asserting Keys in Json are same as our expectations.
    #     response = self.client.get('/users/useractivity/')
    #     self.assertEqual(set(response.json().keys()), {'ok', 'members'})
