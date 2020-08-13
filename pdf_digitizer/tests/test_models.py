from django.test import TestCase, Client
from ..models import InvoiceStructuredData,InvoiceFileUpload


class ModelsTestCase(TestCase):
    def test_model_can_create_invoice_model(self):
        """Tests to check if the User model is able to
            create and save new instance."""

        # count the current User Objects present
        # Create and Save a user, count again and
        # match if both are not equal

        old_count = InvoiceStructuredData.objects.count()
        object = InvoiceStructuredData.objects.create(invoiceid="WNIND6")
        object.invoice_number = "INV1234"
        object.date_of_purchase = "28/12/2018"
        object.save()
        new_count = InvoiceStructuredData.objects.count()
        self.assertNotEqual(old_count, new_count)
        return object

    def test_model_can_upload_invoice(self):
        """Tests to check if the User model is able to
            create and save new instance."""

        # count the current User Objects present
        # Create and Save a user, count again and
        # match if both are not equal

        old_count = InvoiceFileUpload.objects.count()
        c = Client()
        with open('requirements.txt') as fp:
            c.post('/upload/', {'document': fp})
        new_count = InvoiceFileUpload.objects.count()
        self.assertNotEqual(old_count, new_count)



    def test_model_str_representation(self):
        """ Django models may have a __str__ method which drives how the model
        is represented as a string. Test to check the str representation"""

        # Create a User for User Model and check if
        # the String Representation of Object Variable
        # is equal to its real_name field

        user = InvoiceStructuredData.objects.create(invoiceid="90OP98")
        self.assertEqual(str(user), "90OP98")
