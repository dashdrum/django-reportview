"""

Django Reportview is distributed under the terms of the University 
of Illinois/NCSA Open Source License

Copyright (c) 2013 Dan Gentry 
All rights reserved.

Developed by:   Dan Gentry
                Dashdrum
                http://dashdrum.com
                
Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
with the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions:

1) Redistributions of source code must retain the above copyright notice, this list 
of conditions and the following disclaimers.

2) Redistributions in binary form must reproduce the above copyright notice, this 
list of conditions and the following disclaimers in the documentation and/or other 
materials provided with the distribution.

3) Neither the names of Dan Gentry, Dashdrum , nor the names of its contributors 
may be used to endorse or promote products derived from this Software without 
specific prior written permission.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE CONTRIBUTORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.

"""

from django.test import TestCase 
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from reportview.views import ReportMixin, TemplateReportView

from factories import AuthorFactory
from models import Author

class TestReportMixin(TestCase):
    def test_filename(self):
        ## Instantiate object with no filename
        test_object = ReportMixin()
        
        self.assertRaises(ImproperlyConfigured,test_object.get_output_filename)
        
        ## Instantiate object with filename
        test_object = ReportMixin()
        test_object.output_filename='output.pdf'
        
        self.assertEqual(test_object.get_output_filename(),'output.pdf')
    
        
class TestTemplateReportView(TestCase):
    def test_context(self):
        ##  Instantiate object with no context
        test_view = TemplateReportView(output_filename='output.pdf',template_name='template.rml')
        
        ##  Compare to results using Django's TemplateView 
        test_view2 = TemplateView(output_filename='output.pdf',template_name='template.rml')
        
        ## Test with no context
        
        ## get context from each view
        context1 = test_view.get_context_data()
        context2 = test_view2.get_context_data()
        
        ## remove 'view' key from dictionary, if present        
        try:
            del context1['view']
            del context2['view']
        except KeyError:
            pass  ## v1.4 doesn't add this key
        
        self.assertEqual(context1, context2)
        
        ## Test with additional context items added
        
        ## get context from each view
        context1 = test_view.get_context_data(cv = 'test', cv2 = 'test2')
        context2 = test_view2.get_context_data(cv = 'test', cv2 = 'test2')
        
        ## remove 'view' key from dictionary, if present        
        try:
            del context1['view']
            del context2['view']
        except KeyError:
            pass  ## Django v1.4 doesn't add this key
        
        self.assertEqual(context1, context2)
        
    def test_response(self):
        response = self.client.get(reverse('simple_test'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'simpletest.rml')
        self.assertEqual(response['Content-Type'],'application/pdf')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="simpletest.pdf"')
        
class TestDetailReportView(TestCase):
    def test_successful(self):
        aut = AuthorFactory.create()
        response = self.client.get(reverse('detail_test', kwargs = {'pk': aut.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detailtest.rml')
        self.assertEqual(response.context['object'], aut)
        
class TestListReportView(TestCase):
    def test_empty_list(self):
        response = self.client.get(reverse('list_test'))
        self.assertEqual(response.status_code, 200)
        
    def test_no_empty_list(self):
        response = self.client.get(reverse('list_test_no_empty'))
        self.assertEqual(response.status_code, 404)
        
    def test_list(self):
        aut1 = AuthorFactory.create()
        aut2 = AuthorFactory.create()
        aut3 = AuthorFactory.create()
        aut4 = AuthorFactory.create()
        response = self.client.get(reverse('list_test'))
        self.assertTemplateUsed(response, 'listtest.rml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([aut for aut in response.context['object_list']],[aut for aut in Author.objects.all()])
        
        
        
        
        