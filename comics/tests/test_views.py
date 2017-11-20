from django.core.urlresolvers import reverse
from django.test import TestCase

from comics.models import Publisher, Series

class SeriesListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pub, c_pub = Publisher.objects.get_or_create(
            name='DC Comics',
            slug='dc-comics',
            cvid=1)
        # Create 13 test series for pagination tests
        number_of_series = 13
        for ser_num in range(number_of_series):
            Series.objects.create(
                name='Series %s' % ser_num,
                slug='series-%s' % ser_num,
                cvid=ser_num,
                publisher=pub,)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('comics:series-list'))
        self.assertEqual(resp.status_code, 302)

