from django.conf.urls import patterns, include, url

from views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
   
   url(r'^simpletest/$', SimpleReportTest.as_view(), name='simple_test'),
   url(r'^detailtest/(?P<pk>\d+)/$',DetailReportTest.as_view(),name='detail_test'),
   url(r'^listtest/$', ListReportTest.as_view(), name='list_test'),
   
   
   url(r'authorreport/(?P<pk>\d+)/$',AuthorReport.as_view(),name='author_report'),
   url(r'author/(?P<pk>\d+)/$',AuthorDetail.as_view(),name='author'),
   
   url(r'pubreport/$',PublisherReport.as_view(),name='pub_report'),
   url(r'publist/$',PublisherList.as_view(),name='pub_list'),
)
