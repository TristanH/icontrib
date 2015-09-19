from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^register$', 'payments.views.register', name='register')
)
