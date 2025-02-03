from django.test import TestCase
from django.urls import reverse
from myauth.views import get_cookie_view


# Create your tests here.

class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        res = self.client.get(reverse('myauth:get_cookie'))
        self.assertContains(res, 'Cookie value') #Contains проверка на содержимое и статус код

class FooBarViewTestCase(TestCase):
    def test_foo_bar_view(self):
        res = self.client.get(reverse('myauth:foo_bar'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['content-type'], 'application/json')
        expected_data = {'foo': 'bar', 'spam': 'eggs'}
        self.assertJSONEqual(res.content, expected_data)