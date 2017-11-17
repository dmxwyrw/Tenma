import datetime
from django.test import TestCase
from django.utils.text import slugify
from ..models import (Arc, Character, Creator, Issue,
                      Publisher, Series, Team)


class ArcTest(TestCase):

    def setUp(self):
        self.name = 'Another Civil War'
        self.cvid = '1234'
        self.slug = slugify(self.name)

    def test_arc_creation(self):
        a = Arc.objects.create(name=self.name,
                               cvid=self.cvid,
                               slug=self.slug)
        self.assertTrue(isinstance(a, Arc))
        self.assertEqual(a.__str__(), a.name)


class CharacterTest(TestCase):

    def setUp(self):
        self.name = 'The Super Guy'
        self.cvid = '1234'
        self.slug = slugify(self.name)

    def test_character_creation(self):
        c = Character.objects.create(name=self.name,
                                     cvid=self.cvid,
                                     slug=self.slug)
        self.assertTrue(isinstance(c, Character))
        self.assertEqual(c.__str__(), c.name)


class CreatorTest(TestCase):

    def setUp(self):
        self.name = 'Joe Smith'
        self.cvid = '4321'
        self.slug = slugify(self.name)

    def test_creator_creation(self):
        c = Creator.objects.create(name=self.name,
                                   cvid=self.cvid,
                                   slug=self.slug)
        self.assertTrue(isinstance(c, Creator))
        self.assertEqual(c.__str__(), c.name)


class IssueTest(TestCase):

    def setUp(self):
        self.name = 'A Small Step'
        self.number = 1.5
        self.cvid = '5432'
        self.series = SeriesTest.create_series(self)

    def test_issue_creation(self):
        i = Issue.objects.create(name=self.name,
                                 cvid=self.cvid,
                                 number=self.number,
                                 date=datetime.date.today(),
                                 series=self.series,
                                 mod_ts=datetime.date.today())
        self.assertTrue(isinstance(i, Issue))
        self.assertEqual(i.__str__(), self.series.name + ' #' + str(i.number))
        self.assertEqual(i.number, 1.5)
        self.assertEqual(i.date, datetime.date.today())
        self.assertTrue(isinstance(i.series, Series))


class PublisherTest(TestCase):

    def setUp(self):
        self.name = 'DC Comics'
        self.cvid = '9876'
        self.slug = slugify(self.name)

    def test_publisher_creation(self):
        p = Publisher.objects.create(name=self.name,
                                     cvid=self.cvid,
                                     slug=self.slug)
        self.assertTrue(isinstance(p, Publisher))
        self.assertEqual(p.__str__(), p.name)


class SeriesTest(TestCase):

    def create_series(self, name="Long Series", cvid='6543'):
        return Series.objects.create(name=name,
                                     cvid=cvid,
                                     slug=slugify(name))

    def test_series_creation(self):
        s = self.create_series()
        self.assertTrue(isinstance(s, Series))
        self.assertEqual(s.__str__(), s.name)


class TeamTest(TestCase):

    def create_team(self, name="The Greatest Team"):
        return Team.objects.create(name=name)

    def test_team_creation(self):
        t = self.create_team()
        self.assertTrue(isinstance(t, Team))
        self.assertEqual(t.__str__(), t.name)
