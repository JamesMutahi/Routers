from django.urls import path

from web import views

urlpatterns = [
    path('', views.landing_page, name='landing-page'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
]
