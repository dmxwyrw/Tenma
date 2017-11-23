from django.test import TestCase

from ..utils.comicimporter import ComicImporter


class ImporterTest(TestCase):
    def test_series_sort_name(self):
        res = 'Demon, The'
        ci = ComicImporter()
        sort_name = ci.create_series_sortname('The Demon')
        self.assertEqual(res, sort_name)
        