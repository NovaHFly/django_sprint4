from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


class OnlyAuthorMixin(UserPassesTestMixin):
    """Mixin which restricts non-author users from accessing edit page."""

    def test_func(self) -> bool:
        return self.get_object().author == self.request.user

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class RedirectToPostPageMixin:
    def get_success_url(self) -> str:
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']},  # type: ignore
        )


class RedirectToProfileMixin:
    def get_success_url(self) -> str:
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.author.username},  # type: ignore
        )
