from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'icontrib.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'icontrib.views.logout', name='logout'),
    url(r'^setup_payment', 'icontrib.views.cc_form', name='setup_payment'),
    url(r'^done/$', 'icontrib.views.done'),
    url(r'^create_campaign/$', 'icontrib.views.signup', name='create_campaign'),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^payments/', include('payments.urls', namespace='payments'))
)
