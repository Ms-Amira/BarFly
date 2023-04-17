from django.urls import path

from . import views

urlpatterns = [
  path('accounts/signup/', views.signup, name='signup'),
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('bars/', views.cats_index, name='index'),
  path('bars/<int:bar_id>/', views.bars_detail, name='detail'),
  path('bars/create/', views.BarCreate.as_view(), name='bars_create'),
]