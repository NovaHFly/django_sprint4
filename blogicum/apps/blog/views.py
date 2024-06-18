from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from blog.forms import CommentForm, ProfileForm
from blog.models import Category, Post

User = get_user_model()


def view_profile(request: HttpRequest, username: str) -> HttpResponse:
    """View user profile."""
    profile_owner = get_object_or_404(User, username=username)
    return render(
        request,
        template_name='blog/profile.html',
        context={'profile': profile_owner},
    )


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


class Index(ListView):
    model = Post
    ordering = '-pub_date'
    paginate_by = 10
    template_name = 'blog/index.html'
    queryset = Post.objects.select_all_related().get_published_posts()


class PostDetail(DetailView):
    model = Post
    queryset = Post.objects.get_published_posts()
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:  # noqa: A002
    """Show post content.

    Args:
        request (HttpRequest): Request received from the user.
        id (int): Post id.
    """
    template = 'blog/detail.html'
    required_post = get_object_or_404(
        Post.objects.select_all_related().get_published_posts(),
        pk=post_id,
    )

    context = {'post': required_post}
    return render(request, template, context)


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
