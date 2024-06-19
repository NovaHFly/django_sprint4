from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.constants import POSTS_ON_PAGE
from blog.forms import CommentForm, PostForm, ProfileForm
from blog.mixins import (
    OnlyAuthorMixin,
    RedirectToPostPageMixin,
    RedirectToProfileMixin,
)
from blog.models import Category, Comment, Post

User = get_user_model()


class Index(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = POSTS_ON_PAGE

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().select_all_related().get_published()


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .select_all_related()
            .get_all_for_user(self.request.user)
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CreatePost(LoginRequiredMixin, RedirectToProfileMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form: PostForm) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditPost(OnlyAuthorMixin, RedirectToPostPageMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'


class DeletePost(OnlyAuthorMixin, RedirectToProfileMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class ViewProfile(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = POSTS_ON_PAGE

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .select_all_related()
            .get_all_for_user(self.request.user)
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
        return redirect('blog:profile', username=form.instance.username)

    return render(
        request, template_name='blog/user.html', context={'form': form}
    )


class CategoryPosts(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = POSTS_ON_PAGE

    def get_queryset(self) -> QuerySet[Any]:
        self.category = get_object_or_404(
            Category.objects.filter(is_published=True),
            slug=self.kwargs['category_slug'],
        )
        return (
            super()
            .get_queryset()
            .select_all_related()
            .get_published()
            .filter(category__slug=self.kwargs['category_slug'])
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


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


class EditComment(OnlyAuthorMixin, RedirectToPostPageMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .filter(post=get_object_or_404(Post, id=self.kwargs['post_id']))
        )


class DeleteComment(OnlyAuthorMixin, RedirectToPostPageMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .filter(post=get_object_or_404(Post, id=self.kwargs['post_id']))
        )
