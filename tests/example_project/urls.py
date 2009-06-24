from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # serve static files
    (r'^$', 'myapp.views.get_paginated_objects'),

    # reverse url lookups
#    (r'^', include('djangobaselibrary.sample.urls')),

)

