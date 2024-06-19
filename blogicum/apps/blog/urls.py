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
        views.ViewProfile.as_view(),
        name='profile',
    ),
]

posts_patterns = [
    path(
        'posts/<int:post_id>/',
        views.PostDetail.as_view(),
        name='post_detail',
    ),
    path(
        'posts/create/',
        views.CreatePost.as_view(),
        name='create_post',
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.EditPost.as_view(),
        name='edit_post',
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.DeletePost.as_view(),
        name='delete_post',
    ),
]

comment_patterns = [
    path(
        'posts/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment',
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.EditComment.as_view(),
        name='edit_comment',
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.DeleteComment.as_view(),
        name='delete_comment',
    ),
]

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPosts.as_view(),
        name='category_posts',
    ),
    *profile_patterns,
    *posts_patterns,
    *comment_patterns,
]
