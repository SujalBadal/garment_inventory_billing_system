from django.contrib import admin
from .models import Shop, Category, Subcategory, Product

# Register all models here.
admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
