from django.shortcuts import render
from .api_key import get_news
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    country = request.GET.get('country', 'us')
    category = request.GET.get('category', 'general')
    page = int(request.GET.get('page', 1))
    
    news = get_news(country=country, category=category, page=page)
    articles = news.get('articles', [])

    return render(request, 'home/cards.html', {
        'news': articles,
        'country': country,
        'category': category,
        'page': page,
        'has_more': len(articles) == 20 
    })
