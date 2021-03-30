from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from posts.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text')
        labels = {
            'group': _('Имя'),
            'text': _('Текст')
        }
        help_texts = {
            'group': _('Имя группы'),
            'text': _('Текст поста который планируется к публикации')
        }
