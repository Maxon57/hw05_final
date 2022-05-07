from django import forms

from .models import Comment, Group, Post


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea,
                           label='Текст поста',
                           help_text='Текст нового поста',
                           required=True
                           )
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   label='Группа',
                                   help_text='''
                                        Группа к которой
                                        будет относиться пост
                                   ''',
                                   required=False
                                   )

    class Meta:
        model = Post
        fields = ['text', 'group', 'image']


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea,
                           label='Текст комментария',
                           help_text='Текст комментария'
                           )

    class Meta:
        model = Comment
        fields = ['text']
