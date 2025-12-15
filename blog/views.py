from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden
from .models import *

# LOGIN VIEW
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Hoş geldiniz, {request.user.first_name} {request.user.last_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
    
    return redirect('home')

# LOGOUT VIEW
def logout_user(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('home')

# REGISTER VIEW
def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        first_name = (request.POST.get('first_name') or '').strip()
        last_name = (request.POST.get('last_name') or '').strip()
        password1 = request.POST.get('password1') or ''
        password2 = request.POST.get('password2') or ''

        if not username:
            messages.error(request, 'Kullanıcı adı zorunludur!')
            return redirect('register')

        if password1 != password2:
            messages.error(request, 'Şifreler uyuşmuyor!')
            return redirect('register')

        if len(password1) < 6:
            messages.error(request, 'Şifre en az 6 karakter olmalıdır!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu kullanıcı adı zaten kullanılıyor!')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )
        login(request, user)
        messages.success(request, 'Kayıt başarılı. Hoş geldiniz!')
        return redirect('home')

    return render(request, 'register.html')

# HOME VIEW
def home(request):
    category_id = request.GET.get('category')
    
    if request.user.is_authenticated and request.user.is_staff:
        blogs = Blog.objects.all()
    else:
        blogs = Blog.objects.filter(status='p')
    
    if category_id:
        blogs = blogs.filter(category_id=category_id)
    
    categories = Category.objects.all()
    selected_category = category_id
    
    return render(request, 'home.html', {
        'blogs': blogs,
        'categories': categories,
        'selected_category': selected_category
    })

# BLOG DETAIL VIEW
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    
    if blog.status == 'd':
        if not request.user.is_authenticated or (request.user != blog.user and not request.user.is_staff):
            messages.error(request, 'Bu blog henüz yayınlanmamış.')
            return redirect('home')
    
    if request.user.is_authenticated:
        PostViews.objects.get_or_create(
            user=request.user,
            blog=blog,
            defaults={'post_views': True}
        )
    
    comments = blog.comments.all()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Likes.objects.filter(user=request.user, blog=blog, likes=True).exists()
    return render(request, 'blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'user_liked': user_liked,
    })

# BLOG CREATE VIEW
@login_required
def blog_create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden('Bu işlem için yetkiniz yok.')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.POST.get('image')
        category_id = request.POST.get('category')
        status = request.POST.get('status', 'd')
        
        if not request.user.is_staff:
            status = 'd'
        
        blog = Blog.objects.create(
            title=title,
            content=content,
            image=image,
            category_id=category_id,
            user=request.user,
            status=status
        )
        messages.success(request, 'Blog başarıyla oluşturuldu.')
        return redirect('blog_detail', slug=blog.slug)
    
    categories = Category.objects.all()
    return render(request, 'blog_form.html', {'categories': categories})

# BLOG UPDATE VIEW
@login_required
def blog_update(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    
    if request.user != blog.user and not request.user.is_staff:
        return HttpResponseForbidden('Bu blogu düzenleme yetkiniz yok.')
    
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.image = request.POST.get('image')
        blog.category_id = request.POST.get('category')
        
        if request.user.is_staff:
            blog.status = request.POST.get('status', blog.status)
        
        blog.save()
        messages.success(request, 'Blog başarıyla güncellendi.')
        return redirect('blog_detail', slug=blog.slug)
    
    categories = Category.objects.all()
    return render(request, 'blog_form.html', {
        'blog': blog,
        'categories': categories
    })

# BLOG DELETE VIEW
@login_required
def blog_delete(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    
    if request.user != blog.user and not request.user.is_staff:
        return HttpResponseForbidden('Bu blogu silme yetkiniz yok.')
    
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog başarıyla silindi.')
        return redirect('home')
    
    return render(request, 'blog_confirm_delete.html', {'blog': blog})

# COMMENT CREATE VIEW
@login_required
def comment_create(request, slug):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, slug=slug)
        content = request.POST.get('content')
        
        Comment.objects.create(
            user=request.user,
            blog=blog,
            content=content
        )
        messages.success(request, 'Yorum başarıyla eklendi.')
        return redirect('blog_detail', slug=slug)

# COMMENT UPDATE VIEW
@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if request.user != comment.user:
        return HttpResponseForbidden('Bu yorumu düzenleme yetkiniz yok.')
    
    if request.method == 'POST':
        comment.content = request.POST.get('content')
        comment.save()
        messages.success(request, 'Yorum başarıyla güncellendi.')
        return redirect('blog_detail', slug=comment.blog.slug)

    return render(request, 'comment_form.html', {'comment': comment})

# COMMENT DELETE VIEW
@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if request.method != 'POST':
        return HttpResponseForbidden('Geçersiz istek.')

    if request.user != comment.user and not request.user.is_staff:
        return HttpResponseForbidden('Bu yorumu silme yetkiniz yok.')
    
    blog_slug = comment.blog.slug
    comment.delete()
    messages.success(request, 'Yorum başarıyla silindi.')
    return redirect('blog_detail', slug=blog_slug)

# LIKE TOGGLE VIEW
@login_required
def like_toggle(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    like = Likes.objects.filter(user=request.user, blog=blog).first()

    if like is None:
        Likes.objects.create(user=request.user, blog=blog, likes=True)
        liked = True
    else:
        like.likes = not like.likes
        like.save()
        liked = like.likes
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'like_count': blog.get_like_count()
        })
    
    return redirect('blog_detail', slug=slug)

# CATEGORY LIST VIEW
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

# CATEGORY CREATE VIEW
@login_required
def category_create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden('Bu işlem için yetkiniz yok.')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        messages.success(request, 'Kategori başarıyla oluşturuldu.')
        return redirect('category_list')
    
    return render(request, 'category_form.html')

# CATEGORY UPDATE VIEW
@login_required
def category_update(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden('Bu işlem için yetkiniz yok.')
    
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        messages.success(request, 'Kategori başarıyla güncellendi.')
        return redirect('category_list')
    
    return render(request, 'category_form.html', {'category': category})

# CATEGORY DELETE VIEW
@login_required
def category_delete(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden('Bu işlem için yetkiniz yok.')
    
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Kategori başarıyla silindi.')
        return redirect('category_list')
    
    return render(request, 'category_confirm_delete.html', {'category': category})