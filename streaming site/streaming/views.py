from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json

def index(request):
    return render(request, 'index.html')

def signup_view(request):
    """Create a new user only if both fields provided and username is unused."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            # simply reload the form; a real app would show an error
            return render(request, 'signup.html')
        if User.objects.filter(username=username).exists():
            # user exists, let them try logging in instead
            return redirect('login')
        user = User.objects.create_user(username, None, password)
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html')

def login_view(request):
    """Authenticate existing users. Avoid KeyError by using get().
    Pass an error message to the template if credentials are invalid."""
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid username or password."
    return render(request, 'login.html', {'error': error})

def home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    with open('movies.json', 'r') as f:
        movies = json.load(f)
    # pass username explicitly in case template context processor isn't available
    return render(request, 'home.html', {'movies': movies, 'username': request.user.username})

def movie_detail(request, movie_id):
    if not request.user.is_authenticated: return redirect('login')
    if request.session.get('has_paid'):
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return redirect('subscribe', movie_id=movie_id)

def subscribe_page(request, movie_id):
    # only signed-in users should see the paywall
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'subscribe.html', {'movie_id': movie_id})

def process_payment(request):
    # protect endpoint, otherwise someone could hit it directly
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        request.session['has_paid'] = True
        return render(request, 'success.html')
    return redirect('home')


def payment_success(request):
    # called by JS; mark session paid and reply with JSON
    if request.method == 'POST':
        request.session['has_paid'] = True
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'invalid method'}, status=400)

def logout_view(request):
    logout(request)
    return redirect('index')