from .models import Category

def category_list(request):
    # Veritabanındaki tüm kategorileri çekiyoruz
    categories = Category.objects.all()
    # Bu sözlük, projedeki TÜM template'lerde 'all_categories' ismiyle kullanılabilir olacak
    return {
        'all_categories': categories
    }