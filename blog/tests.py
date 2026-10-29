from django.test import TestCase
from django.urls import reverse

from .models import Comments, Post


class ReadLaterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(
            title='A saved post',
            excerpt='A sample excerpt.',
            content='This is the content of a sample blog post.',
            slug='saved-post',
        )
        cls.other_post = Post.objects.create(
            title='Another post',
            excerpt='Another sample excerpt.',
            content='This is the content of another blog post.',
            slug='other-post',
        )

    def test_read_later_saves_post_and_redirects_to_list(self):
        response = self.client.post(
            reverse('read_later', kwargs={'slug': self.post.slug}),
        )

        self.assertRedirects(response, reverse('stored_posts'))
        self.assertEqual(self.client.session['stored_posts'], [self.post.pk])
        response = self.client.get(reverse('stored_posts'))
        self.assertTemplateUsed(response, 'blog/stored-post.html')
        self.assertQuerySetEqual(
            response.context['stored_posts'], [self.post],
        )
        self.assertContains(
            response,
            reverse('post_detail', kwargs={'slug': self.post.slug}),
        )

    def test_saving_same_post_twice_does_not_duplicate_it(self):
        url = reverse('read_later', kwargs={'slug': self.post.slug})
        self.client.post(url)
        self.client.post(url)

        self.assertEqual(self.client.session['stored_posts'], [self.post.pk])

    def test_saving_another_post_preserves_existing_selection(self):
        for post in (self.post, self.other_post):
            self.client.post(reverse('read_later', kwargs={'slug': post.slug}))

        self.assertEqual(
            self.client.session['stored_posts'],
            [self.post.pk, self.other_post.pk],
        )

    def test_stored_posts_is_empty_for_new_session(self):
        response = self.client.get(reverse('stored_posts'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No stored posts.')
        self.assertQuerySetEqual(response.context['stored_posts'], [])

    def test_missing_post_returns_404_without_changing_session(self):
        response = self.client.post(
            reverse('read_later', kwargs={'slug': 'missing-post'}),
        )

        self.assertEqual(response.status_code, 404)
        self.assertNotIn('stored_posts', self.client.session)


class PostCommentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(
            title='A sample post',
            excerpt='A sample excerpt.',
            content='This is the content of a sample blog post.',
            slug='sample-post',
            image='blogs/sample.jpg',
        )

    def setUp(self):
        self.url = reverse('post_detail', kwargs={'slug': self.post.slug})

    def test_get_displays_comment_fields(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="content"')
        self.assertContains(response, 'Submit Comment')

    def test_valid_comment_is_saved_for_post_and_redirects(self):
        response = self.client.post(self.url, {
            'name': 'Alice',
            'email': 'alice@example.com',
            'content': 'This was a helpful post.',
        })

        self.assertRedirects(response, self.url)
        comment = Comments.objects.get()
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.name, 'Alice')
        self.assertEqual(comment.email, 'alice@example.com')
        self.assertEqual(comment.content, 'This was a helpful post.')
        self.client.get(self.url)
        self.assertEqual(Comments.objects.count(), 1)

    def test_invalid_comment_preserves_values_and_displays_errors(self):
        response = self.client.post(self.url, {
            'name': 'Alice',
            'email': 'invalid-email',
            'content': 'Hi',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['form'].errors), {'email', 'content'})
        self.assertContains(response, 'value="Alice"')
        self.assertContains(response, 'value="invalid-email"')
        self.assertContains(response, 'comment-field errors', count=2)
        self.assertContains(response, 'Enter a valid email address.')
        self.assertEqual(Comments.objects.count(), 0)

    def test_missing_post_does_not_save_comment(self):
        response = self.client.post(
            reverse('post_detail', kwargs={'slug': 'missing-post'}),
            {'name': 'Alice', 'email': 'alice@example.com', 'content': 'A comment.'},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Comments.objects.count(), 0)
