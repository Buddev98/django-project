from django.test import TestCase
from django.urls import reverse


class ReviewViewsTests(TestCase):
    def test_valid_review_redirects_to_thank_you(self):
        response = self.client.post(
            reverse('review_list'),
            {'username': 'Test User', 'review': 'A helpful review.'},
        )

        self.assertRedirects(response, reverse('thank_you'))
        self.assertEqual(response.url, '/reviews/thank_you/')

    def test_thank_you_page(self):
        response = self.client.get(reverse('thank_you'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/thank_you.html')
        self.assertContains(response, 'Thank you for your review!')

    def test_invalid_review_shows_form_errors(self):
        response = self.client.post(reverse('review_list'), {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/reviews.html')
        self.assertContains(response, 'Please enter your name')
        self.assertContains(response, 'Please enter your review')
