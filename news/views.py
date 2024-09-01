from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from allauth.account.forms import LoginForm, SignupForm
from .api_key import get_news

# Create your views here.
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

# User input confirmation message
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            messages.success(request, "You have successfully logged in.")
            return redirect('home')
        else:
            messages.error(request, "Login failed. Please check your credentials and try again.")
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})

def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully signed up.")
            return redirect('home')
        else:
            messages.error(request, "Signup failed. Please check the form and try again.")
    else:
        form = SignupForm()

    return render(request, 'account/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')