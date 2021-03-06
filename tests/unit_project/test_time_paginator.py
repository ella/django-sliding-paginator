from urllib import unquote_plus
from datetime import datetime

from djangosanetesting import DatabaseTestCase, UnitTestCase

from djangoslidingpaginator.paginators import SlidingPkPaginator

from myapp.models import Comment

class TestProperSlicing(DatabaseTestCase):

    def setUp(self):
        super(TestProperSlicing, self).setUp()

        first = [
            Comment.objects.create(
                text = u"Comment %s" % 0,
                date = datetime(year=2000, month=1, day=1, hour=1, minute=1)
            )
        ]

        fluff = [
            Comment.objects.create(
                text = u"Comment %s" % i
            )
            for i in xrange(1, 50)
        ]
        
        last = [
            Comment.objects.create(
                text = u"Comment %s" % 50,
                date = datetime(year=2050, month=1, day=1, hour=1, minute=1)
            )
        ]

        self.comments = first + fluff + last
        # we want newest first
        self.comments.reverse()

    def assert_comments_equals(self, expected, got):
        for obj in expected:
            matched = [i for i in got if i == obj]
            if len(matched) < 1:
                raise AssertionError("Expected object %s not retrieved in %s" % (
                    obj, got
                ))

    def test_default_slicing(self):
        paginator = SlidingPkPaginator(Comment.objects.all().order_by('-pk'))
        self.assert_comments_equals(self.comments[0:10], paginator.get_objects())

    def test_custom_slicing(self):
        paginator = SlidingPkPaginator(Comment.objects.all().order_by('-pk'), on_page=20)
        self.assert_comments_equals(self.comments[0:20], paginator.get_objects())

    def test_id_anchored_slicing(self):
        paginator = SlidingPkPaginator(Comment.objects.all().order_by('-pk'),
            anchor = self.comments[1].pk
        )
        self.assert_comments_equals(self.comments[1:11], paginator.get_objects())

class TestFormAction(UnitTestCase):
    def setUp(self):
        super(TestFormAction, self).setUp()
        self.paginator = SlidingPkPaginator([], anchor=1)

    def test_default_action_is_current_page(self):
        self.assert_equals(".", self.paginator.form_action)

    def test_paginator_with_reverse_lookup(self):
        self.paginator.view_name = "myapp-objects"
        self.assert_equals("/1/10/", unquote_plus(self.paginator.form_action))

    def test_post_parsing_anchor(self):
        self.paginator.parse_post({
                'anchor' : 1,
            }
        )
        self.assert_equals(1, self.paginator.anchor)
        
