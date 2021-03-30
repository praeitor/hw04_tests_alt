from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import reverse


from posts.models import Post, Group
from posts.forms import PostForm

User = get_user_model()


def index(request):
    latest = Post.objects.all()[:10]
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'posts': latest, 'page': page}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'group.html',
        {'group': group, 'posts': posts, 'page': page}
    )


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('index')
    return render(request, 'newpost.html', {'form': form})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'posts': posts,
        'page': page,
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    post = Post.objects.get(pk=post_id)
    profile = get_object_or_404(User, username=username)
    context = {
        'profile': profile,
        'post': post
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    post = Post.objects.get(pk=post_id)
    if post.author != request.user:
        return redirect('post', username, post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.author = request.user
            form.save()
            return redirect(reverse(
                'post',
                kwargs={'username': username, 'post_id': post_id})
            )
        else:
            form = PostForm(instance=post)
    form = PostForm(instance=post)
    return render(
        request,
        'newpost.html',
        {'form': form, 'post': post, 'is_edit': True}
    )
