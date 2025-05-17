from .models import Category

def get_all_categories(request):
    return dict(all_categories = Category.objects.all())