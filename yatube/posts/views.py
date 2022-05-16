from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User
from .utils import check_user, install_paginator


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
                                        'author').annotate(
        count_comments=Count('comments')).filter(author_id=author.pk)
    following = Follow.objects.filter(author_id=author.pk,
                                      user_id=request.user.pk).exists()
    profile_info = User.objects.annotate(
        follower_count=Count('follower', distinct=True),
        following_count=Count('following', distinct=True),
        count_posts=Count('user_info', distinct=True)).get(user=author.username)
    context = {
        'page_obj': install_paginator(request, posts),
        'author': author,
        'following': following,
        'profile_info': profile_info
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
    form = PostForm(request.POST or None,
                    files=request.FILES or None
                    )
    if form.is_valid():
        save_form = form.save(commit=False)
        save_form.author_id = request.user.pk
        save_form.save()
        return redirect('posts:profile', username=request.user.username)
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = Post.objects.select_related('author').get(pk=post_id)
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
    if post.author.pk == request.user.pk:
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
    posts = Post.objects.filter(author__following__user=request.user)
    context = {
        'page_obj': install_paginator(request, posts)
    }
    return render(request, 'posts/follow.html', context)


@check_user
@login_required
def profile_follow(request, username):
    user = get_object_or_404(User, username=username)
    Follow.objects.create(author=user,
                          user=request.user
                          )
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    user = get_object_or_404(User, username=username)
    user_unfollow = Follow.objects.filter(author=user,
                                          user=request.user
                                          )
    if user_unfollow.exists():
        user_unfollow.delete()
    return redirect('posts:profile', username)
