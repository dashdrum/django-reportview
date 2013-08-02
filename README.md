# Django ReportView

Based on PDFGenView by Inka Labs

<http://inka-labs.com/blog/2013/04/12/generating-pdfs-was-never-so-easy/>
         
Django ReportView provides drop-in replacements for generic class-based views that send the output to a PDF file.  The same code used to generate a web page can be repurposed to create a printable copy.
 
The trml2pdf libary is used to convert a ReportLab template (RML) to PDF output.  
 
Each view adds a class variable called `output-filename`, which holds the name of the file to be created.

## Dependencies

- Django 1.3+ <https://www.djangoproject.com/>
- reportlab <http://www.reportlab.com/>
- trml2pdf <https://github.com/roadhead/trml2pdf>

## ReportMixin

This mixin holds the key code from the Inka Labs example.

The `get` method is where all of the magic happens. After setting up the MIME type and filename for the `response`, the RML template is rendered using standard Django code. Trml2pdf takes takes the rendered template and outputs a PDF file.  One should take care when overriding this method as to not break this functionality.  (Hopefully there won't be much reason to.)

Also, the code to set and check for the `output-filename` variable is here.  In this version, the functionality of SingleObjectTemplateResponseMixin and MultipleObjectTemplateResponseMixin have not been implemented.

This mixin should be used with TemplateResponseMixin and View in the inheritence chain.

## TemplateReportView

Mimicking the function of Django's TemplateView, TemplateReportView will output a template, including any context provided.

### Example

    class SimpleReportTest(TemplateReportView):
        template_name = 'simpletest.rml'
        output_filename = 'simpletest.pdf'
    
        def get_context_data(self,**kwargs):
            context = super(SimpleReportTest,self).get_context_data(**kwargs)
            context['name'] = 'Simple Report Test'
            return context
    
## DetailReportView

Used to generate a report based on a single object.  Just like the generic DetailView, the programmer should provide a template name and data source (model or queryset), along with the output filename.

### Example

    class AuthorReport(DetailReportView):
        template_name = 'author_report.rml'
        model = Author
        output_filename = 'author_report.pdf'     
           
`get_context_data()` may be overriden to provide additional context to the template, but the `super` call must be included, since the object value is set in the parent class.  (See the TempleReportView example.)

The URL definition should pass a `pk` or `slug` variable to the class.

    url(r'authorreport/(?P<pk>\d+)/$',AuthorReport.as_view(),name='author_report'),

## ListReportView

ListReportView follows the function of ListView to send a list of objects to be rendered into a report. A template name, data source (model or queryset), and output filename should be provided.

At this point, I haven't done anything with the pagination settings, so they will be ignored.

### Example

    class PublisherReport(ListReportView):
        template_name = 'pub_report.rml'
        model = Publisher
        output_filename = 'pub_report.pdf'
       
Once again, 'get_context_data()' should be overridden including a `super` call, in this case to set the `object-list` class variable.

## RML Templates

RML is a very rich templating language included in the ReportLab package.  I have only begun to explore the possibilities, so there are just a few basic examples provided in this release.  

## Version History



### Version 0.1 - May 5, 2013 

Initial release


## License

Django Reportview is distributed under the terms of the University of Illinois/NCSA Open Source License license.

<http://otm.illinois.edu/uiuc_openSource>
       
     