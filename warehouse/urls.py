from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products_list_view, name='products_list'),
    path('replenish/<int:count>/', views.replenish_view, name='replenish'),
    path('', views.products_list_view, name='home'),
]