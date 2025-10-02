from django.shortcuts import render


def index(request):
    """Ana sayfa"""
    return render(request, 'core/index.html')


def about(request):
    """Hakkında sayfası"""
    return render(request, 'core/about.html')
