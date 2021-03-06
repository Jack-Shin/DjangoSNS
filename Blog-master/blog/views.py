from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Post, Comment, Heart
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User


# List of posts on homepage
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

# List of unpublished posts (drafts)
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True, author=request.user).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

# Detailed page for a post
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    isAuthor = False
    if post.author == request.user:
        isAuthor = True

    return render(request, 'blog/post_detail.html', {'post': post, 'isAuthor' : isAuthor})

# Form to add a new post
@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

# Form to edit a post
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        return redirect('post_list')
    else:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post_detail', post_id=post.pk)
        else:
            form = PostForm(instance=post)
    
    return render(request, 'blog/post_edit.html', {'form': form})

# Publish a post
@login_required
def post_publish(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        post.publish()
    return redirect('post_detail', post_id=post_id)

# Remove a post
@login_required
def post_remove(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        post.delete()
    return redirect('post_list')

# Form to add a comment to a post
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})

# Remove a comment
@login_required
def remove_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('post_detail', post_id=comment.post.pk)

# Approve a comment
@login_required
def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.approve()
    return redirect('post_detail', post_id=comment.post.pk)

def heart_post(request, post_id):
    if request.user.is_authenticated():
        username = request.user
        try:
            heart = Heart.objects.get(post_id = post_id, lover = username)
            heart.delete()
        except Heart.DoesNotExist:
            post = get_object_or_404(Post, pk = post_id)
            heart = Heart(lover = username, post = post)
            heart.save()
            
    n = getCountHeart(post_id)
    return render(request, 'blog/heart_post.html', { 'n' : n })
    

def nheart_post(request, post_id):
    n = getCountHeart(post_id)
    return render(request, 'blog/heart_post.html', { 'n' : n })


def getCountHeart(post_id):
    p = get_object_or_404(Post, pk=post_id)
    n = Heart.objects.filter(post=p).count()
    return n

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pw = request.POST['pw']
        rpw = request.POST['rpw']

        if pw == rpw:
            print(username)
            try:
                user = User.objects.get(username = username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, email=email, password=pw)
                user.save()
                return redirect('/')

        return render(request, 'registration/signup.html', {})
    else:
        return render(request, 'registration/signup.html', {})