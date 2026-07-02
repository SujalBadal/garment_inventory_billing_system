from django.db import models

class Shop(models.Model):
    owner_name = models.CharField(max_length=100)
    shop_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.shop_name

class Category(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('shop', 'name')

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('shop', 'category', 'name')

    def __str__(self):
        return f"{self.category.name} -> {self.name}"

class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField()
    rack_location = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    class Meta:
        unique_together = ('shop', 'product_id')

    def __str__(self):
        return self.name
