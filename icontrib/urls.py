from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'icontrib.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'icontrib.views.logout', name='logout'),

    url(r'^start/?$', 'icontrib.views.start', name='start'),
    url(r'^setup_payment/?$', 'icontrib.views.cc_form', name='setup_payment'),
    url(r'^done/?$', 'icontrib.views.done'),

    url(r'^create_campaign/?$', 'icontrib.views.create_campaign', name='create_campaign'),
    url(r'^view_campaign/(\w+)$', 'icontrib.views.view_campaign', name='view_campaign'),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^payments/', include('payments.urls', namespace='payments'))
)
