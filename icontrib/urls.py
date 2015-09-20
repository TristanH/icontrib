from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'icontrib.views.start', name='start'),

    url(r'^campaign/?$', 'icontrib.views.create_campaign', name='campaign'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/?$', 'icontrib.views.logout', name='logout'),

    url(r'^pay/?$', 'icontrib.views.setup_payments', name='setup_payment'),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^payments/', include('payments.urls', namespace='payments'))
)
