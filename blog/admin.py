from django.contrib import admin
from .models import Category, Post, ReadingHistory, VideoProgress

admin.site.site_header = "Modern Blog Yönetim Paneli"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "Hoş Geldiniz, İçeriklerinizi Buradan Yönetebilirsiniz"

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User



# Kullanıcı sayfasının içine gömülecek tablo
class VideoProgressInline(admin.TabularInline):
    model = VideoProgress
    fields = ('video_url', 'formatted_position', 'updated_at') # Görünecek alanlar
    readonly_fields = ('formatted_position', 'updated_at') # Sadece okunabilir
    extra = 0

class ReadingHistoryInline(admin.StackedInline):
    model = ReadingHistory
    extra = 0

# Standart User Admin'i genişletiyoruz
class UserAdmin(BaseUserAdmin):
    inlines = (VideoProgressInline, ReadingHistoryInline)

# Mevcut User Admin'i silip yenisini kaydediyoruz
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Yazı listesinde hangi sütunlar görünecek?
    list_display = ('title', 'slug', 'author', 'created_on','seo_title','seo_description')
    
    # Sağ tarafa filtreleme seçenekleri ekler
    list_filter = ("author", "created_on",)
    
    # Arama kutusu hangi alanlarda arama yapacak?
    search_fields = ['title', 'content']
    
    # Başlık yazılırken slug kısmını otomatik doldurur (Modern URL yapısı için)
    prepopulated_fields = {'slug': ('title',)}
    
    # Uzun listelerde sayfalama yapar
    list_per_page = 20

    # Formu gruplandırarak SEO alanlarını ayırabiliriz
    fieldsets = (
        ('İçerik Bilgileri', {
            'fields': ('title', 'slug', 'category', 'author', 'content', 'image', 'youtube_video_id')
        }),
        ('SEO Ayarları', {
            'fields': ('seo_title', 'seo_description'),
            'description': 'Arama motorları için optimize edilmiş başlık ve açıklama.'
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['youtube_video_id'].label = "YouTube Video Linki"
        return form

