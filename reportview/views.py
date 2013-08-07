####  Django ReportView
#
#     A mixin and class-based views to facilitate the creation of PDF reports
#     using ReportLab and trml2pdf. Stock Django CBV mixins are used, so the
#     interface to the programmer mimics that of DetailView and ListView.
#
#     Based on PDFGenView by Inka Labs
#         http://inka-labs.com/blog/2013/04/12/generating-pdfs-was-never-so-easy/
# 
####

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

from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

import trml2pdf


class ReportMixin(object):
    ''' Based on PDFGenView by Inka Labs - http://inka-labs.com/blog/2013/04/12/generating-pdfs-was-never-so-easy/
    
        Uses trm2pdf library to generate a PDF report from a ReportLab template 
        
        Use with TemplateResponseMixin and View  '''
    
    output_filename = None

    def get_output_filename(self):
        if self.output_filename is None:
            raise ImproperlyConfigured('%s requires either a definition of '
                                       'output_filename or an implementation '
                                       'of get_output_filename()'
                                       % self.__class__.__name__)
        return self.output_filename

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; filename="%s"'
                                           % self.get_output_filename())
        rml = render_to_string(self.get_template_names(),
                               self.get_context_data())
        if isinstance(rml, unicode):
            rml = rml.encode('UTF-8')
        response.write(trml2pdf.parseString(rml))
        return response
    
### Django v1.4 and 1.5 handle context differently
try:  
    ### Use the mixin provided in v1.5
    from django.views.generic.base import ContextMixin
except ImportError: 
    ### or create a class using the v1.4 functionality
    class ContextMixin(object):
        def get_context_data(self, **kwargs):
            return {
                    'params': kwargs
                   }

class TemplateReportView(ReportMixin, TemplateResponseMixin, ContextMixin, View):
    ''' A simple report - use get_context_data to provide content '''
    pass

class DetailReportView(ReportMixin, TemplateResponseMixin, SingleObjectMixin, View):
    ''' A report based on a single object '''
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DetailReportView,self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ### Add self.object to the context
        return super(DetailReportView,self).get_context_data(object = self.get_object(), **kwargs)
    
class ListReportView(ReportMixin, TemplateResponseMixin, MultipleObjectMixin, View):
    ''' A report based on a list of objects '''
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        return super(ListReportView,self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ### add object_list to the context
        return super(ListReportView,self).get_context_data(object_list=self.get_queryset(), **kwargs)
    
