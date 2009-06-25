from django.http import HttpResponse

def get_paginated_objects(request, on_site=None, anchor=None):

    return HttpResponse("""
       on_site : %s
       anchor : %s
    """ % (str(on_site), str(anchor)))
