from django.http import HttpResponse

def get_paginated_objects(request, on_page=None, anchor=None):

    return HttpResponse("""
       on_page : %s
       anchor : %s
    """ % (str(on_page), str(anchor)))
