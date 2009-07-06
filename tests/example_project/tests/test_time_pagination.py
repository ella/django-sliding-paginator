from djangosanetesting import SeleniumTestCase

from djangoslidingpaginator.paginators import SlidingTimePaginator

from time import sleep
from myapp.models import Comment

class TestPagination(SeleniumTestCase):

    def setUp(self):
        super(TestPagination, self).setUp()

        self.comments = [
            Comment.objects.create(
                text = u"Comment %s" % i
            )
            for i in xrange(0, 150+1)
        ]
        # we want newest first
        self.comments.reverse()
        self.paginator = SlidingTimePaginator(Comment.objects.all().order_by('-date'), on_page=10)

        self.transaction.commit()

        self.selenium.open("/")


    def test_reverse_works(self):
        self.assert_equals(u"Comment 150", self.selenium.get_text("//ul/li[position()=1]"))

    def test_default_slicing_range(self):
        self.assert_equals(10, int(self.selenium.get_xpath_count("//ul/li")))
        self.assert_equals(u"Comment 141", self.selenium.get_text("//ul/li[position()=10]"))

