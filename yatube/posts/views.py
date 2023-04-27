from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post, Group
from .forms import PostForm
from .utils import paginator, pagin_page


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    page_obj = pagin_page(post_list, request.GET.get('page'))
    contents = {
        'page_obj': page_obj,
        'text_desc': 'Последние обновления на сайте'
    }
    return render(request, 'posts/index.html', contents,)


def groups(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all().order_by('-pub_date')
    page_obj = pagin_page(post_list, request.GET.get('page'))
    contents = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', contents)


def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author_id__exact=user_obj
                                    ).order_by('-pub_date')
    user_num_of_posts = paginator(post_list).count
    page_obj = pagin_page(post_list, request.GET.get('page'))
    context = {
        'page_obj': page_obj,
        'user_obj': user_obj,
        'user_num_of_posts': user_num_of_posts,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author_num_posts = Post.objects.filter(author_id__exact=post.author
                                           ).count()
    context = {
        'post': post,
        'author_num_posts': author_num_posts,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
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
    is_edit = True
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    context = {'form': form, 'is_edit': is_edit,
               'post_id': post_id}
    return render(request, 'posts/create_post.html', context)
