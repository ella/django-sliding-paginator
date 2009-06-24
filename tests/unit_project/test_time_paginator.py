from djangosanetesting import DatabaseTestCase

from djangoslidingpaginator.paginators import SlidingTimePaginator

from myapp.models import Comment

class TestProperSlicing(DatabaseTestCase):

    def setUp(self):
        super(TestProperSlicing, self).setUp()

        self.comments = [
            Comment.objects.create(
                text = u"Comment %s" % i
            )
            for i in xrange(0, 50)
        ]
        # we want newest first
        self.comments.reverse()
        self.paginator = SlidingTimePaginator(Comment.objects.all().order_by('-date'), on_page=10)


    def assert_comments_equals(self, expected, got):
        for obj in expected:
            matched = [i for i in got if i == obj]
            if len(matched) < 1:
                raise AssertionError("Expected object %s not retrieved in %s" % (
                    obj, got
                ))

    def test_default_slicing(self):
        self.assert_comments_equals(self.comments[0:10], self.paginator.get_objects())

    def test_custom_slicing(self):
        self.assert_comments_equals(self.comments[0:20], self.paginator.get_objects(on_page=20))

    def test_time_anchored_slicing(self):
        self.assert_comments_equals(self.comments[1:11], self.paginator.get_objects(
            anchor = self.comments[1].date
        ))

