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

from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string

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

class TemplateReportView(ReportMixin, TemplateResponseMixin, View):
    ''' A simple report - use get_context_data to provide content '''

    def get_context_data(self,**kwargs):
        ### start with empty context
        context = {}
        return context

class DetailReportView(ReportMixin, TemplateResponseMixin, SingleObjectMixin, View):
    ''' A report based on a single object '''

    def get_context_data(self, **kwargs):
        ### Add self.object to the context
        self.object = self.get_object()
        context = super(DetailReportView,self).get_context_data( **kwargs)
        context['object'] = self.object
        return context
    
class ListReportView(ReportMixin, TemplateResponseMixin, MultipleObjectMixin, View):
    ''' A report based on a list of objects '''
    
    def get_context_data(self, **kwargs):
        ### allow_empty test
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        ### add self.object_list to the context
        return super(ListReportView,self).get_context_data(object_list=self.object_list, **kwargs)
    
