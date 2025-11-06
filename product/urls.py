from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.category_list_create),
    path('categories/<int:pk>/', views.category_detail),

    path('products/', views.product_list_create),
    path('products/<int:pk>/', views.product_detail),
    path('products/reviews/', views.product_with_reviews),

    path('reviews/', views.review_list_create),
    path('reviews/<int:pk>/', views.review_detail),
]