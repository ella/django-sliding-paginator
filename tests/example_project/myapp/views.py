from django.views.generic.simple import direct_to_template
from djangoslidingpaginator.paginators import SlidingTimePaginator

from myapp.models import Comment


def get_paginated_objects(request):
    comments = Comment.objects.all().order_by('-date')
    paginator = SlidingTimePaginator(comments, on_page=10)

    return direct_to_template(request, "comments.html", {
        'comments' : paginator.get_objects(),
        'paginator' : paginator,
    })
