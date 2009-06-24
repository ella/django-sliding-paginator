-------------------------
Django Sliding Paginator
-------------------------

Django sliding paginator allows You to easily create and handle "sliding" pagination for your sites. Imagine you have listing with lot of object and You want to paginate them.

First way is to use `Django's build-in paginator <http://www.djangoproject.com/documentation/models/pagination/>`_. Disadvantage of this style is:

* You have to know how many objects are in the listing in total, which can be too resource-consuming
* If you have too many objects, displaying pages is ugly (consider > 100 pages)

Other approach would be displaying only "previous" and "next" links, but this is annoying for users that want to control how many objects are displayed on page.

django-sliding-paginator supports combined approach: User can choose how many objects he wants to display on page, and can use links to navigate back and forth, together with "first" and "last" links. Standard form looks like this:

    <<   <   __20__   >  >>

====================
Usage
====================

When working with time-based data, use SlidingTimePaginator

    from djangoslidingpaginator import SlidingTimePaginator
    from myapp.models import Model
    
    objs = Model.objects.all()
    paginator = SlidingTimePaginator(objs, on_page=20, time_attibute="date")


Render form using
    
    {% sliding_paginator from=50 on_page=20 %}


====================
Inner workings
====================

SlidingTimePaginator is used to display data that are changed frequently, to avoid "pages" concept alltogether to prevent data to slide under users hands[#fSliding]_. To anchor data, timestamp is thus used, assumed to be present on model object.

For dealing with non-time based data, SlidingObjectPaginator could be used, anchoring probably on object ID - if it would be implemented. If You're interested in using it, consider `forking us on github <http://github.com/ella/django-sliding-pagination/tree/master>`_ :-)


.. rubric:: Footnotes

.. [#fSliding] Consider having 10 article on page and going to second one. Meanwhile, someone added 10 new objects that are now displayed on first page. Thus, if user will go on third page, he will confusingly see same data as before.
