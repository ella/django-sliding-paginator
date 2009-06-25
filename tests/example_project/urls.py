from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^/$', 'myapp.views.get_paginated_objects', name="myapp-objects"),
)

