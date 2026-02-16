import math
from django.db import models
from ckeditor.fields import RichTextField # Bu satırı ekle
from django.urls import reverse
from django.utils.html import strip_tags # HTML etiketlerini temizlemek için
import re # URL içinden ID'yi ayıklamak için Regex (Düzenli İfadeler) kullanacağız
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories" # Admin panelinde düzgün görünmesi için

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True) # URL için (örn: /blog/ilk-yazim)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField() # CKEditor kullanarak zengin metin alanı
    seo_title = models.CharField(max_length=70, blank=True, help_text="Google başlığı (Boş bırakırsanız yazı başlığı otomatik olarak kopyalanır.)")
    seo_description = models.CharField(max_length=160, blank=True, help_text="Boş bırakırsanız içerikten otomatik özet oluşturulur.")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    image = CloudinaryField('image', null=True, blank=True)
    youtube_video_id = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        help_text="YouTube video linkini buraya yapıştırın (Örn: https://www.youtube.com/watch?v=jNQXAC9IVRw)"
    )

    class Meta:
        ordering = ['-created_on'] # En yeni en üstte
    
    def save(self, *args, **kwargs):
        # 1. SEO Başlığı boşsa, normal başlığı kopyala
        if not self.seo_title:
            self.seo_title = self.title

        # 2. SEO Açıklaması boşsa, içerikten otomatik özet oluştur
        if not self.seo_description:
            # Önce CKEditor'den gelen HTML etiketlerini temizle
            clean_content = strip_tags(self.content)
            # İlk 157 karakteri al ve sonuna ... ekle
            self.seo_description = clean_content[:157] + "..."
        if self.youtube_video_id:
            # Daha kapsayıcı ve temiz bir Regex
            pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
            match = re.search(pattern, self.youtube_video_id)
            if match:
                self.youtube_video_id = match.group(1)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    
    def __cl_image_url__(self):
        if self.image:
            return self.image.url
        return None

    def __str__(self):
        return self.title
    

class ReadingHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='history')
    last_post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.last_post.title if self.last_post else 'Yok'}"
    
class VideoProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_url = models.CharField(max_length=255) # YouTube linki veya ID'si
    last_position = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'video_url')
    
    def formatted_position(self):
        # Saniyeyi dakika ve saniyeye bölüyoruz
        minutes = math.floor(self.last_position / 60)
        seconds = math.floor(self.last_position % 60)
        # 02:05 gibi görünmesi için :02d formatını kullanıyoruz
        return f"{minutes:02d}:{seconds:02d}"
    
    # Admin panelinde sütun başlığı ne görünsün?
    formatted_position.short_description = 'Kaldığı Süre'
