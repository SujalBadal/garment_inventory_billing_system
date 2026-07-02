from django.urls import path
from . import views

urlpatterns = [
    # auth& Dashboard
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('change-password/', views.change_password, name='change_password'),
    
    
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    
    
    path('subcategories/', views.subcategories_list, name='subcategories_list'),
    path('subcategories/edit/<int:subcategory_id>/', views.edit_subcategory, name='edit_subcategory'),
    path('subcategories/delete/<int:subcategory_id>/', views.delete_subcategory, name='delete_subcategory'),
    
   
    path('products/', views.products_list, name='products_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<str:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<str:product_id>/', views.delete_product, name='delete_product'),
    path('products/details/<str:product_id>/', views.product_details, name='product_details'),
]
