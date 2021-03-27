from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.forms import PostForm
from posts.models import Group, Post


class PostsCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = get_user_model()
        cls.guest_client = Client()
        cls.user = user.objects.create(username="user_test")
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title="Тестовый заголовок",
            slug="test-slug",
            description="Описание тестовой группы"
        )
        cls.post = Post.objects.create(
            text="Тестовый тест",
            pub_date="06.01.2021",
            author=PostsCreateFormTests.user,
            group=PostsCreateFormTests.group
        )
        cls.form = PostForm()

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {"text": "Тестовый тест2", "group": self.group.id}
        response = self.authorized_client.post(
            reverse("new_post"),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(text="Тестовый тест2").exists())

    def test_edit_post(self):
        posts_count = Post.objects.count()
        form_data = {
            "text": "Запись после редактирования",
            "group": self.group.id,
        }
        response = self.authorized_client.post(
            "/user_test/1/edit/",
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count == posts_count)
        self.assertTrue(Post.objects.filter(
            text="Запись после редактирования").exists()
        )
        self.assertRedirects(
            response,
            reverse(
                "post",
                kwargs={"username": self.post.author, "post_id": self.post.id}
            )
        )
