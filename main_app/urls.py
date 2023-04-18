from django.urls import path

from . import views

urlpatterns = [
  path('accounts/signup/', views.signup, name='signup'),
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('bars/', views.bars_index, name='index'),
  path('bars/<int:bar_id>/', views.bars_detail, name='detail'),
  path('bars/create/', views.BarCreate.as_view(), name='bars_create'),
  path('bars/<int:pk>/update/', views.BarUpdate.as_view(), name='bars_update'),
  path('bars/<int:bar_id>/assoc_beverage/<int:beverage_id>/', views.assoc_beverage, name='assoc_beverage'),
  path('bars/<int:bar_id>/add_review/', views.add_review, name='add_review'),
  path('beverages/', views.BeverageList.as_view(), name='beverages_index'),
  path('beverages/<int:pk>/', views.BeverageDetail.as_view(), name='beverages_detail'),
  path('beverages/create/', views.BeverageCreate.as_view(), name='beverages_create'),
  path('beverages/<int:pk>/update/', views.BeverageUpdate.as_view(), name='beverages_update'),
  path('beverages/<int:pk>/delete/', views.BeverageDelete.as_view(), name='beverages_delete'),

]