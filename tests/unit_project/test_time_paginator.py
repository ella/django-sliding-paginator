from urllib import unquote_plus
from datetime import datetime
from django.utils.http import urlquote_plus

from djangosanetesting import DatabaseTestCase, UnitTestCase

from djangoslidingpaginator.paginators import SlidingTimePaginator

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
        paginator = SlidingTimePaginator(Comment.objects.all().order_by('-date'))
        self.assert_comments_equals(self.comments[0:10], paginator.get_objects())

    def test_custom_slicing(self):
        paginator = SlidingTimePaginator(Comment.objects.all().order_by('-date'), on_page=20)
        self.assert_comments_equals(self.comments[0:20], paginator.get_objects())

    def test_time_anchored_slicing(self):
        paginator = SlidingTimePaginator(Comment.objects.all().order_by('-date'),
            anchor = self.comments[1].date
        )
        self.assert_comments_equals(self.comments[1:11], paginator.get_objects())

class TestFormAction(UnitTestCase):
    def setUp(self):
        super(TestFormAction, self).setUp()
        self.paginator = SlidingTimePaginator([], anchor=datetime(year=2000, month=1, day=1, hour=1, minute=1))

    def test_default_action_is_current_page(self):
        self.assert_equals(".", self.paginator.form_action)

    def test_paginator_with_reverse_lookup(self):
        self.paginator.view_name = "myapp-objects"
        self.assert_equals("/2000-01-01T01:01:00/10/", unquote_plus(self.paginator.form_action))

    def test_post_parsing_anchor(self):
        dt = datetime(year=2000, month=1, day=1, hour=1, minute=1)
        self.paginator.parse_post({
                'anchor' : urlquote_plus(dt.isoformat()),
            }
        )
        self.assert_equals(dt, self.paginator.anchor)
        
    def test_post_parsing_anchor_with_microseconds(self):
        dt = datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1, microsecond=2)
        self.paginator.parse_post({
                'anchor' : urlquote_plus(dt.isoformat()),
            }
        )
        self.assert_equals(dt, self.paginator.anchor)
