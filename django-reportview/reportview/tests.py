
from django.test import TestCase 
from django.core.exceptions import ImproperlyConfigured

from views import ReportMixin

class TestReportMixin(TestCase):
    def test_filename(self):
        ## Instantiate object with no filename
        test_object = ReportMixin()
        
        self.assertRaises(ImproperlyConfigured,test_object.get_output_filename)
        
        ## Instantiate object with filename
        test_object = ReportMixin()
        test_object.output_filename='output.pdf'
        
        self.assertEqual(test_object.get_output_filename(),'output.pdf')
        
        