from textwrap import shorten

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        verbose_name="текст сообщения",
        help_text="введите сообщение",
    )
    pub_date = models.DateTimeField(
        "date published",
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    group = models.ForeignKey(
        "Group",
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True
    )

    def __str__(self):
        text = shorten(
            f"{self.text}, "
            f"написал {self.author} "
            f"из группы {self.group}, "
            f"дата {self.pub_date}", 
            15,
        )
        return text

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Текст сообщения"


class Group(models.Model):
    title = models.CharField(
        verbose_name="назавание группы",
        help_text="введите название группы",
        max_length=200,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Описание группы"
