from django.urls import path
from . import views

urlpatterns = [
  
    path('billing/', views.billing_screen, name='billing_screen'),
    path('billing/add/', views.add_to_cart, name='add_to_cart'),
    path('billing/remove/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('billing/clear/', views.clear_cart, name='clear_cart'),
    path('billing/checkout/', views.checkout, name='checkout'),
    
    path('invoice/<str:invoice_number>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/print/<str:invoice_number>/', views.invoice_print, name='invoice_print'),
    
    
    path('history/', views.sales_history, name='sales_history'),
]
