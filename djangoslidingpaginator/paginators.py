
class SlidingTimePaginator(object):
    def __init__(self, queryset, on_page=10, time_attribute="date", anchor=None, descending=True):
        super(SlidingTimePaginator, self).__init__()

        self.queryset = queryset
        self.on_page = on_page
        self.time_attribute = time_attribute
        self.anchor = anchor
        if descending:
            self.sort = "lte"
        else:
            self.sort = "gte"

    def get_objects(self, on_page=None, anchor=None):
        on_page = on_page or self.on_page
        anchor = anchor or self.anchor

        if anchor:
            self.queryset = self.queryset.filter(**{
                self.time_attribute+"__"+self.sort : anchor
            })
        return self.queryset[0:on_page]
