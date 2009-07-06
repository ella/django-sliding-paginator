from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'myapp.views.get_paginated_objects', name="myapp-objects"),
)

