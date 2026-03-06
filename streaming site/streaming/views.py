from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

def home(request):
    if 'user' not in request.session:
        return redirect('login')
    with open('movies.json', 'r') as f:
        movies = json.load(f)
    return render(request, 'home.html', {'movies': movies})

def movie_detail(request, movie_id):
    # If they paid, send them to the Rick Roll
    if request.session.get('has_paid'):
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    # Otherwise, show the subscription page
    return redirect('subscribe', movie_id=movie_id)

def subscribe_page(request, movie_id):
    return render(request, 'subscribe.html', {'movie_id': movie_id})

def process_payment(request):
    if request.method == 'POST':
        request.session['has_paid'] = True
        return render(request, 'success.html')
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        request.session['user'] = request.POST.get('username')
        return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')