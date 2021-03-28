from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group

User = get_user_model()


class PostsViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        tuser = User.objects.create(username="user_test")
        cls.group = Group.objects.create(
            title="testgroup",
            slug="tgrp",
            description="testovaya gruppa",
        )
        cls.post = Post.objects.create(
            text="супер пост",
            pub_date="2021-03-22",
            author=tuser,
            group=cls.group,
        )

    def setUp(self):
        self.user = User.objects.get(username="user_test")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_about_page_uses_correct_template(self):
        """Страница group сформирована с правильным шаблоном."""
        response = self.authorized_client.get(
            reverse("group", kwargs={"slug": "tgrp"})
        )
        self.assertTemplateUsed(response, "group.html")

    def test_pages_uses_core_template_auth(self):
        """Страницы index/newpost сформированы с правильным шаблоном."""
        templates_url_names = {
            "index.html": "index",
            "newpost.html": "new_post",
        }
        for template, name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse(name))
                self.assertTemplateUsed(response, template)

    def test_index_page_shows_correct_context(self):
        """Страница index сформирована с правильным контекстом."""
        response = self.authorized_client.get(reverse("index"))
        first_object = response.context["posts"][0]
        paginator = response.context.get("page")
        post_author = first_object.author
        post_text = first_object.text
        self.assertEqual(str(post_author), "user_test")
        self.assertEqual(post_text, "супер пост")
        self.assertEqual(len(paginator), 1)

    def test_group_page_shows_correct_context(self):
        """Страница group сформирована с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("group", kwargs={"slug": "tgrp"})
        )
        self.assertEqual(
            response.context["group"].title, "testgroup"
        )
        self.assertEqual(
            response.context["group"].description, "testovaya gruppa"
        )
        self.assertEqual(response.context["group"].slug, "tgrp")

    def test_newpost_page_shows_correct_context(self):
        """Страница newpost сформирована с правильным контекстом."""
        response = self.authorized_client.get(reverse("new_post"))
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_editpost_page_shows_correct_context(self):
        """Страница editpost сформирована с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            "post_edit",
            kwargs={"username": self.post.author, "post_id": self.post.id})
        )
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_profile_page_shows_correct_context(self):
        """Страница profiles сформирована с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            "profile", args=[self.post.author])
        )
        profile_object = response.context["profile"]
        post_object = response.context["posts"][0]
        profile_username = profile_object.username
        post_text = post_object.text
        self.assertEqual(str(profile_username), "user_test")
        self.assertEqual(post_text, "супер пост")

    def test_post_page_shows_correct_context(self):
        """Страница post сформирована с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            "post",
            kwargs={"username": self.post.author, "post_id": self.post.id})
        )
        post_object = response.context["post"]
        profile_object = response.context["profile"]
        profile_username = profile_object.username
        post_text = post_object.text
        self.assertEqual(str(profile_username), "user_test")
        self.assertEqual(post_text, "супер пост")
