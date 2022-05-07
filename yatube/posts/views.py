from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User
from .utils import install_paginator


def index(request):
    post_list = Post.objects.select_related('group', 'author').all()
    context = {
        'page_obj': install_paginator(request, post_list),
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_info.select_related('author').all()
    context = {
        'group': group,
        'page_obj': install_paginator(request, posts),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.select_related('group',
                                        'author').filter(author_id=author.pk)
    following = Follow.objects.filter(author_id=request.user.pk,
                                      user_id=author.pk).exists()
    context = {
        'page_obj': install_paginator(request, posts),
        'author': author,
        'following': following
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    detail_post = Post.objects.select_related('author',
                                              'group').get(pk=post.pk)
    count_posts = Post.objects.filter(author_id=detail_post.author.pk).count()
    comments = Comment.objects.select_related('author').filter(post_id=post_id)
    context = {
        'detail_post': detail_post,
        'count_posts_author': count_posts,
        'form': CommentForm(),
        'comments': comments
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.author_id = request.user.pk
            save_form.save()

            return redirect('posts:profile', username=request.user.username)
    form = PostForm()
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = Post.objects.select_related('author').get(pk=post_id)
    if request.method == 'POST':
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
            instance=post)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.author_id = request.user.pk
            save_form.pk = post_id
            save_form.save()
            return redirect('posts:post_detail', post_id)
    else:
        if post.author.pk == request.user.pk:
            form = PostForm(instance=post)
            context = {'form': form,
                       'is_edit': True,
                       'post_id': post_id
                       }
            return render(request, 'posts/create_post.html', context)
        else:
            return redirect('users:login')


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = Post.objects.get(pk=post_id)
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    users = Follow.objects.filter(author_id=request.user.pk)
    posts = Post.objects.filter(author_id__in=[
        user.user_id for user in users
    ])
    context = {
        'page_obj': install_paginator(request, posts)
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    if username != request.user.username:
        user = get_object_or_404(User, username=username)
        Follow.objects.create(author_id=request.user.pk,
                              user_id=user.pk
                              )
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    if username != request.user.username:
        user = get_object_or_404(User, username=username)
        Follow.objects.get(author_id=request.user.pk,
                           user_id=user.pk
                           ).delete()
    return redirect('posts:profile', username)
