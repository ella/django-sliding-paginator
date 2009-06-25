from django.views.generic.simple import direct_to_template
from djangoslidingpaginator.paginators import SlidingPkPaginator

from myapp.models import Comment


def get_paginated_objects(request, on_page=None, anchor=None):
    comments = Comment.objects.all().order_by('-date')
    paginator = SlidingPkPaginator(comments, on_page=10)

    return direct_to_template(request, "comments.html", {
        'comments' : comments,
        'paginator' : paginator,
    })
