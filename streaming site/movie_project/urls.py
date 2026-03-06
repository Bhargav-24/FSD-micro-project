from django.urls import path
from streaming import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/subscribe/', views.subscribe_page, name='subscribe'),
    path('process-payment/', views.process_payment, name='process_payment'),
]