from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('post_list')

    return render(request, 'login.html')


@login_required
def post_list(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

@login_required
def view_all_posts(request):
    query = request.GET.get('q')   # get search query

    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all()

    return render(request, 'view_all_posts.html', {
        'posts': posts,
        'query': query
    })
@login_required
def create_post(request):
    form = PostForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('post_list')

    return render(request, 'post_form.html', {'form': form})


@login_required
def update_post(request, id):

    post = get_object_or_404(Post, id=id)

    if request.user != post.author and not request.user.is_superuser:
        return redirect('post_list')

    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('post_list')

    return render(request, 'post_form.html', {'form': form})


@login_required
def delete_post(request, id):

    post = get_object_or_404(Post, id=id)

    if request.user != post.author and not request.user.is_superuser:
        return redirect('post_list')

    post.delete()

    return redirect('post_list')


def logout_view(request):
    logout(request)
    return redirect('login')