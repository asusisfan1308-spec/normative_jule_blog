from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from .models import Post, Like
from .forms import PostForm, ContactForm


# День 1, 6, 7, 8, 9: Вывод, поиск и пагинация
def post_list(request):
    query = request.GET.get('q', '')
    posts = Post.objects.all().order_by('-created_at')

    if query:
        # Расширенный поиск по заголовку ИЛИ контенту (День 7)
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    count = posts.count()  # Количество найденных (День 7)

    # Пагинация по 5 постов (День 8)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'q': query,
        'count': count
    })


# День 5, 10: Детальная страница поста и счетчик лайков
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(user=request.user, post=post).exists()

    return render(request, 'blog/post_detail.html', {'post': post, 'liked': liked})


# День 5: Создание поста (защита)
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


# День 3: Регистрация
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


# День 11: Переключатель лайка
@login_required
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # Если лайк уже был - удаляем
    return redirect('post_detail', pk=pk)


# День 12: Отправка письма
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                f"Xabar {name} dan",
                message,
                email,
                ['admin@blog.uz'],
                fail_silently=False,
            )
            return render(request, 'blog/contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})


from django.shortcuts import render

# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('login')

