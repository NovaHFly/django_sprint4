from django.contrib import admin

from blog.models import Category, Comment, Location, Post


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
    )
    list_display_links = ('title',)
    list_editable = ('is_published',)
    search_fields = ('title',)
    inlines = (PostInline,)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_display_links = ('name',)
    list_editable = ('is_published',)
    search_fields = ('name',)
    inlines = (PostInline,)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'is_published',
        'pub_date',
        'category',
        'location',
    )
    list_display_links = ('id', 'title')
    list_editable = ('is_published', 'category', 'location')
    list_filter = ('category', 'location')
    search_fields = ('title', 'text', 'author__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at', 'is_published', 'post')
    list_display_links = ('id',)
    list_editable = ('is_published',)
    search_fields = ('author__username',)
