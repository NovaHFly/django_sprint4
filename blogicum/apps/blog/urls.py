from django.http import HttpResponse
from django.urls import path

from blog import views

app_name = 'blog'

profile_patterns = [
    path(
        'profile/edit/',
        views.edit_profile,
        name='edit_profile',
    ),
    path(
        'profile/<str:username>/',
        views.view_profile,
        name='profile',
    ),
]

posts_patterns = [
    path(
        'posts/create/',
        lambda x: HttpResponse('Create new post!'),
        name='create_post',
    ),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path(
        'posts/<int:post_id>/edit_post/',
        lambda x, post_id: HttpResponse(f'Edit post {post_id}'),
        name='edit_post',
    ),
    path(
        'posts/<int:post_id>/delete/',
        lambda x, post_id: HttpResponse(f'Delete post {post_id}'),
        name='delete_post',
    ),
]

comment_patterns = [
    path(
        'posts/<int:post_id>/comment/',
        lambda x, post_id: HttpResponse(f'Add comment to post {post_id}'),
        name='add_comment',
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        lambda x, post_id, comment_id: HttpResponse(
            f'Edit comment {comment_id} at post {post_id}'
        ),
        name='edit_comment',
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        lambda x, post_id, comment_id: HttpResponse(
            f'Delete comment {comment_id} from post {post_id}'
        ),
        name='delete_comment',
    ),
]

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts',
    ),
    *profile_patterns,
    *posts_patterns,
    *comment_patterns,
]
