from django.db import models


class Publishable(models.Model):
    """Add is_published field."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )

    class Meta:
        abstract = True


class ContainsCreateDate(models.Model):
    """Add created_at field which autofills with object creation date."""

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
