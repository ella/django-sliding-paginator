from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<anchor>.+)?/(?P<on_page>\d+)?/$', 'myapp.views.get_paginated_objects', name="myapp-objects"),
)

