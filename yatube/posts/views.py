from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post, Group, Comment
from .forms import PostForm, CommentForm
from .utils import pagin_page


def index(request):
    post_list = Post.objects.all()
    page_obj = pagin_page(post_list, request.GET.get('page'))
    contents = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', contents,)


def groups(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = pagin_page(post_list, request.GET.get('page'))
    contents = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', contents)


def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    post_list = user_obj.posts.all()
    user_num_of_posts = user_obj.posts.count()
    page_obj = pagin_page(post_list, request.GET.get('page'))
    context = {
        'page_obj': page_obj,
        'user_obj': user_obj,
        'user_num_of_posts': user_num_of_posts,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(
        post_id__exact=post_id).order_by('-created')
    form = PostForm(
        request.POST or None,
    )
    if form.is_valid():
        add_comment(request, post_id)
    context = {
        'post': post,
        'author_num_posts': post.author.posts.count(),
        'comments': comments,
        'form': form
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:profile', username=post.author)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not request.user == post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'is_edit': True,
        'post_id': post_id
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)
