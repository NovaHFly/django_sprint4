from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from blog.forms import ProfileForm
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


def index(request: HttpRequest) -> HttpResponse:
    """Show project main page.

    Args:
        request (HttpRequest): Request received from the user.
    """
    template = 'blog/index.html'

    posts = Post.objects.select_all_related().get_published_posts()[:5]
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:  # noqa: A002
    """Show post content.

    Args:
        request (HttpRequest): Request received from the user.
        id (int): Post id.
    """
    template = 'blog/detail.html'
    required_post = get_object_or_404(
        Post.objects.select_all_related().get_published_posts(),
        pk=id,
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
