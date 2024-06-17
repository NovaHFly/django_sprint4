from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from core.models import (
    ContainsCreateDate,
    Publishable,
)

User = get_user_model()


class PostQuerySet(models.QuerySet):
    """Custom query set for post model."""

    def get_published_posts(self) -> models.QuerySet:
        """Fetch posts which are published.

        Published posts are not either:
        1. Have is_published flag set to False.
        2. Belong to category with is_published flag set to False.
        3. Have pub_date greater than now.
        """
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )

    def select_all_related(self) -> models.QuerySet:
        """Select all foreign keys for the posts."""
        return self.select_related('author', 'category', 'location')


class Category(Publishable, ContainsCreateDate):
    """Category of posts by the same theme."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены'
            ' символы латиницы, цифры, дефис и подчёркивание.'
        ),
    )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Location(Publishable, ContainsCreateDate):
    """Some landmark."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name


class Post(Publishable, ContainsCreateDate):
    """A single post."""
    # TODO: Add images

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем'
            ' — можно делать отложенные публикации.'
        ),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория',
    )

    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return f'{self.pub_date} - {self.title}'
