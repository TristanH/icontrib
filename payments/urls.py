from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^client_token/$', 'payments.views.generate_client_token')
)
