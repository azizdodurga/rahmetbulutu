from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.postgres.search import SearchVector # PostgreSQL'e özel araç
from django.db.models import Q # "Veya" sorguları yapabilmek için gerekli
from .models import Category, Post, ReadingHistory, VideoProgress
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.http import require_POST



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Kullanıcı oluşunca ona bir geçmiş kaydı oluştur
            ReadingHistory.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Yazı detay sayfasında kaldığı yeri güncelleme mantığı
from django.shortcuts import render, get_object_or_404
from .models import Post, ReadingHistory, VideoProgress # VideoProgress modelini eklemeyi unutma

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user_progress = None # Başlangıçta boş tanımlıyoruz
    
    # Eğer kullanıcı giriş yapmışsa işlemleri yap
    if request.user.is_authenticated:
        # 1. Okuma Geçmişini Güncelle (Senin mevcut kodun)
        history, created = ReadingHistory.objects.get_or_create(user=request.user)
        history.last_post = post
        history.save()

        # 2. Videoda Kaldığı Yeri Veritabanından Çek
        # Bu veri, HTML içindeki JavaScript'e 'nereden başlayacağını' söyleyecek
        user_progress = VideoProgress.objects.filter(
            user=request.user, 
            video_url=post.youtube_video_id
        ).first()
        
    return render(request, 'post_detail.html', {
        'post': post, 
        'user_progress': user_progress # Şablona (Template) gönderiyoruz
    })



def post_list(request):
    query = request.GET.get('q') # Arama kutusundan gelen veri
    
    # 1. Önce tüm veya filtrelenmiş veriyi çekiyoruz
    if query:
        # Bir arama yapılmışsa: Başlık ve içerikte PostgreSQL ile ara
        posts = Post.objects.annotate(
            search=SearchVector('title', 'content'),
        ).filter(search=query)
    else:
        # Arama yoksa tüm liste
        posts = Post.objects.all().order_by('created_on')

    # 2. Sayfalama mantığını HER DURUMDA çalıştırıyoruz
    paginator = Paginator(posts, 6) # Sayfa başı 6 yazı
    page_number = request.GET.get('page')
    
    # page_obj değişkeni burada kesin olarak tanımlanıyor
    page_obj = paginator.get_page(page_number)

    # 3. Şablona page_obj gönderiliyor
    return render(request, 'index.html', {
        'page_obj': page_obj, 
        'query': query
    })

def category_detail(request, slug):
    # 1. Kategoriyi bul, yoksa 404 döndür
    category = get_object_or_404(Category, slug=slug)
    
    # 2. Bu kategoriye ait yazıları çek
    post_list = Post.objects.filter(category=category).order_by('-created_on')
    
    # 3. Sayfalama (Pagination) ekle - Şablonun hata vermemesi için şart!
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 4. 'index.html' şablonunu tekrar kullanıyoruz (kod tekrarından kaçınmak için)
    return render(request, 'index.html', {
        'page_obj': page_obj, 
        'category': category
    })

@require_POST
def save_video_progress(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'login_required'}, status=401)

    video_id = request.POST.get('video_id')
    position = request.POST.get('position')

    if video_id and position:
        # Kullanıcı ve video ID'sine göre kaydı güncelle veya yoksa oluştur
        VideoProgress.objects.update_or_create(
            user=request.user,
            video_url=video_id, # Modelindeki alan adıyla aynı olmalı
            defaults={'last_position': float(position)}
        )
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'invalid_data'}, status=400)


