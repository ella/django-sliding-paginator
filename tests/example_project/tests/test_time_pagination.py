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
            for i in xrange(0, 150)
        ]
        # we want newest first
        self.comments.reverse()
        self.paginator = SlidingTimePaginator(Comment.objects.all().order_by('-date'), on_page=10)

        self.transaction.commit()

        self.selenium.open("/")


    def test_default_slicing(self):
        sleep(10)

