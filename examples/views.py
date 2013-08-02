from reportview.views import TemplateReportView, DetailReportView, ListReportView
from django.views.generic import DetailView, ListView
from models import Author, Book, Publisher, Store
    
class SimpleReportTest(TemplateReportView):
    template_name = 'simpletest.rml'
    output_filename = 'simpletest.pdf'
    
    def get_context_data(self,**kwargs):
        context = super(SimpleReportTest,self).get_context_data(**kwargs)
        context['name'] = 'Simple Report Test'
        return context
    
class DetailReportTest(DetailReportView):
    template_name = 'detailtest.rml'
    model = Author
    output_filename = 'detailtest.pdf'
        
class ListReportTest(ListReportView):
    template_name = 'listtest.rml'
    queryset = Book.objects.all()
    output_filename = 'listtest.pdf'
    
class AuthorDetail(DetailView):
    template_name = 'author.html'
    model = Author
    
class AuthorReport(DetailReportView):
    template_name = 'author_report.rml'
    model = Author
    output_filename = 'author_report.pdf'

class PublisherList(ListView):
    template_name = 'pub_list.html'
    model = Publisher
    
class PublisherReport(ListReportView):
    template_name = 'pub_report.rml'
    model = Publisher
    output_filename = 'pub_report.pdf'
    