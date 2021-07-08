from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, Http404
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

import random

from .models import Post
from .forms import PostForm


def index(request):
    if request.user.is_authenticated:
        topic_query = request.GET.get('topic', None)
        search_query = request.GET.get('search', None)
            
        if not search_query and not topic_query:
            posts = Post.objects.all()

        elif search_query and not topic_query:
            posts = Post.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query)).distinct()
        
        elif not search_query and topic_query:
            posts = Post.objects.filter(Q(topic__icontains=topic_query)).distinct()
        
        else:
            posts = Post.objects.filter(topic=topic_query)
            posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query)).distinct()

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        featured_posts = Post.objects.filter(featured=True)

        context = {
            'posts': page_obj,
            'featured_posts': featured_posts[:3],
            'recent_posts': Post.objects.all()[:3],
        }

        return render(request, 'post/index.html', context)
    else:
        return render(request, 'post/home.html', {})


# TODO the options may be the same, fix it
@login_required
def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    recent_posts = Post.objects.all()[:3]
    may_like_posts = random.choices(list(Post.objects.all()[:10]), k=2)

    context = {
        'post': post,
        'recent_posts': recent_posts,
        'may_like_posts': may_like_posts,
    }

    return render(request, 'post/detail.html', context)


def create(request):
    if request.user.is_superuser:
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post:index')

        context = {
            'form': form,
            'title': 'Create',
        }

        return render(request, 'post/form.html', context)
    else:
        raise Http404()


def update(request, slug):
    if request.user.is_superuser:
        post = get_object_or_404(Post, slug=slug)
        form = PostForm(request.POST or None, request.FILES or None, instance=post)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post.get_absolute_url())

        context = {
            'form': form,
            'title': 'Update',
        }

        return render(request, 'post/form.html', context)
    else:
        raise Http404()


def delete(request, slug):
    if request.user.is_superuser:
        post = get_object_or_404(Post, slug=slug)
        post.delete()

        return redirect('post:index')
    else:
        raise Http404()

"""
@login_required
def contact(request):
    return render(request, 'post/contact.html', {})
"""
