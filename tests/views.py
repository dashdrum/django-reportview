from reportview.views import TemplateReportView, DetailReportView, ListReportView
from models import Author
        
class TemplateReportViewSimple(TemplateReportView):
    template_name = 'simpletest.rml'
    output_filename = 'simpletest.pdf'
    
    def get_context_data(self,**kwargs):
        context = super(TemplateReportViewSimple,self).get_context_data(**kwargs)
        context['name'] = 'Simple Report Test'
        return context
    
class DetailReportViewSimple(DetailReportView):
    template_name = 'detailtest.rml'
    output_filename = 'detailtest.pdf'
    model = Author
    
class ListReportViewSimple(ListReportView):
    template_name = 'listtest.rml'
    output_filename = 'listtest.pdf'
    model = Author
    
class ListReportViewSimpleNoEmpty(ListReportView):
    template_name = 'listtest.rml'
    output_filename = 'listtest.pdf'
    model = Author
    allow_empty = False