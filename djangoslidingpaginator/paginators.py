from django.core.urlresolvers import reverse
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from django.utils.http import urlquote_plus
from djangoslidingpaginator.forms import PaginationForm

DEFAULT_ON_PAGE = 10

class SlidingPkPaginator(object):
    def __init__(self, queryset, on_page=DEFAULT_ON_PAGE, sort_attribute="pk",
        anchor=None, descending=True, view_name=None):
        super(SlidingPkPaginator, self).__init__()

        self.queryset = queryset
        self.on_page = on_page
        self.sort_attribute = sort_attribute
        self.anchor = anchor
        self.view_name = view_name
        if descending:
            self.sort = "lte"
        else:
            self.sort = "gte"

    def get_objects(self):
        if self.anchor:
            self.queryset = self.queryset.filter(**{
                self.sort_attribute+"__"+self.sort : self.anchor
            })
        return self.queryset[0:self.on_page]

    def parse_post(self, post):
        if post.has_key('on_page'):
            self.on_page = int(post['on_page'])

        if post.has_key('anchor'):
            self.anchor = int(post['anchor'])

    def get_form_buttons(self):
        form = PaginationForm({'on_page' : self.on_page})
        if not form.is_valid():
            form = PaginationForm({'on_page' : DEFAULT_ON_PAGE})
        try:
            return mark_safe(render_to_string("djangoslidingpaginator/paginator_time_form.html", {
                "form" : form,
            }))
        except TemplateDoesNotExist:
            # user has not overwritten our default, which we will provide here
            #FIXME: Find a non-hacky way to distribute template that would be globally available
            return mark_safe("""<button value="<<" name="pagination_first" type="submit">&lt;&lt;</button>
                <button value="<" name="pagination_back" type="submit">&lt;</button>
                %s
                <button value=">" name="pagination_forward" type="submit">&gt;</button>
                <button value=">>" name="pagination_last" type="submit">&gt;&gt;</button>
            """ % str(form['on_page']))

    def get_form(self):
        return mark_safe("""<form action="%s" method="post">%s</form>""" % (
            self.get_form_action(),
            self.get_form_buttons()
        ))

    form = property(fget=get_form)

    def get_form_action(self):
        if not self.view_name or not self.anchor:
            return '.'
        else:
            return reverse(
                self.view_name,
                kwargs = {
                    "anchor" : urlquote_plus(unicode(self.anchor)),
                    "on_page" : self.on_page,
                }
            )

    form_action = property(fget=get_form_action)
