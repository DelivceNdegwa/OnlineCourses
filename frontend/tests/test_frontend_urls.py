from django.test import SimpleTestCase
from django.urls import reverse, resolve
from frontend import views


class URLTests(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse("frontend:home")
        self.assertEqual(resolve(url).func, views.index)