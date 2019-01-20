from django.test import TestCase


from post.models import Post

class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Post.objects.create(title='Test post')

    def test_title_label(self):
        post=Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')

    def test_title_max_length(self):
        post=Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length,200)

    def test_object_name_is_last_name_comma_first_name(self):
        post=Post.objects.get(id=1)
        expected_object_name = '%s' % (post.title)
        self.assertEquals(expected_object_name,str(post))

    def test_get_absolute_url(self):
        post=Post.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(post.get_absolute_url(),'/post/post/1')
