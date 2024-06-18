from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.forms import CommentForm, PostForm, ProfileForm
from blog.models import Category, Post

User = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        return self.get_object().author == self.request.user


class Index(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/index.html'
    queryset = Post.objects.select_all_related().get_published_posts()


class PostDetail(DetailView):
    model = Post
    queryset = Post.objects.get_published_posts()
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CreatePost(CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def get_success_url(self) -> str:
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )

    def form_valid(self, form: PostForm) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditPost(OnlyAuthorMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def get_success_url(self) -> str:
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class DeletePost(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'form.instance'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context

    def get_success_url(self) -> str:
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class ViewProfile(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/profile.html'

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .select_all_related()
            .filter(author__username=self.kwargs['username'])
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile_owner = get_object_or_404(
            User, username=self.kwargs['username']
        )
        context['profile'] = profile_owner
        return context


@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    """Edit user profile."""
    current_user = request.user
    form = ProfileForm(request.POST or None, instance=current_user)

    if form.is_valid():
        form.save()
        return render(
            request,
            template_name='blog/profile.html',
            context={'profile': current_user},
        )

    return render(
        request, template_name='blog/user.html', context={'form': form}
    )


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Show list of posts in a category.

    Args:
        request (HttpRequest): Request received from the user.
        category_slug (str): Category identifier.
    """
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug,
    )
    posts = category.posts.select_all_related().get_published_posts()
    context = {'category': category.title, 'post_list': posts}
    return render(request, template, context)


@login_required
def add_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_id)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('blog:post_detail', post_id=post_id)
