from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'icontrib.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'icontrib.views.logout'),
    url(r'^signup/$', 'icontrib.views.signup'),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('payments.urls', namespace='payments'))
)
