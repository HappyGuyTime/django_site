# import json
from django.test import TestCase
from django.urls import reverse

class GetCookieViewTestCase(TestCase):
    def test_add_two_numbers(self):
        response = self.client.get(reverse("myauth:get_cookie"))
        self.assertContains(response, "Cookie value")


class FooBarViewTest(TestCase):
    def test_foo_bar_view(self):
        response = self.client.get(reverse("myauth:foo-bar"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')

        expected_data = {'foo': 'bar', 'spam': 'eggs'}
        self.assertJSONEqual(response.content, expected_data)
        # received_data = json.loads(response.content)
        # self.assertEqual(received_data, expected_data)