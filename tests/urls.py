from django.conf.urls import patterns, url

from views import TemplateReportViewSimple, DetailReportViewSimple, ListReportViewSimple, ListReportViewSimpleNoEmpty

urlpatterns = patterns('',
   url(r'^simpletest/$', TemplateReportViewSimple.as_view(), name='simple_test'),
   url(r'^detailtest/(?P<pk>\d+)/$',DetailReportViewSimple.as_view(),name='detail_test'),  
   url(r'^listtest/$', ListReportViewSimple.as_view(), name='list_test'),  
   url(r'^listtestnoempty/$', ListReportViewSimpleNoEmpty.as_view(), name='list_test_no_empty'), 
)
