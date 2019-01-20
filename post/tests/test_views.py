from django.test import TestCase

# Create your tests here.

from post.models import Post
from django.urls import reverse

class PostListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Create 8 authors for pagination tests
        number_of_posts = 8
        for post_num in range(number_of_posts):
            Post.objects.create(title='Post %s' % post_num)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/post/posts/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('posts'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('posts'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'post/post_list.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('posts'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['post_list']) == 5)

    def test_lists_all_posts(self):
        #Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('posts')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['post_list']) == 3)
