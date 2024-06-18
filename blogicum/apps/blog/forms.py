import django.forms as forms
from django.contrib.auth import get_user_model

from blog.models import Comment

User = get_user_model()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
