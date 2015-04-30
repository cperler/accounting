from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'money.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^update/(?P<account_id>\d+)$', 'accounting.views.update', name='update'),
    url(r'^refresh_all$', 'accounting.views.refresh_all', name='refresh-all'),
    url(r'index', 'accounting.views.index', name='index')
)
