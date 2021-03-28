from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Post, Group

User = get_user_model()


class PostsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        tuser = User.objects.create(username="user_test")
        Post.objects.create(
            text="супер пост",
            pub_date="2021-01-20",
            author=tuser,
        )
        cls.uverif = Post.objects.get(pk=1)

    def test_post_verbose(self):
        post = PostsModelTest.uverif
        verbosetext = post._meta.get_field("text").verbose_name
        self.assertEqual(verbosetext, "текст сообщения")

    def test_post_helptext(self):
        post = PostsModelTest.uverif
        helptext = post._meta.get_field("text").help_text
        self.assertEqual(helptext, "введите сообщение")

    def test_post_title(self):
        post = PostsModelTest.uverif
        expected = "супер [...]"
        self.assertEquals(expected, str(post))


class GroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(
            title="супер название группы",
            slug="gruppa",
            description="test_group",
        )
        cls.gverif = Group.objects.get(pk=1)

    def test_group_verbose(self):
        group = GroupModelTest.gverif
        verbosetext = group._meta.get_field("title").verbose_name
        self.assertEqual(verbosetext, "назавание группы")

    def test_group_helptext(self):
        group = GroupModelTest.gverif
        helptext = group._meta.get_field("title").help_text
        self.assertEqual(helptext, "введите название группы")

    def test_group_title(self):
        group = GroupModelTest.gverif
        expected = "супер название группы"
        self.assertEquals(expected, str(group))
