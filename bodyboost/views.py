from django.http import JsonResponse
from django.shortcuts import render
from store.models import ProductVariant, Category, ProductVariant


def health_check(request):
    """Simple health check endpoint for Render port detection"""
    return JsonResponse({"status": "ok"}, status=200)


def home(request):

    context = {
        'variants': ProductVariant.objects.all().filter(is_active=True)[:4],
        'all_categories': Category.objects.all()
    }

    return render(request,'home.html', context)