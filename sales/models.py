from django.db import models
from inventory.models import Shop, Product

class Invoice(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    invoice_number = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20) # Cash, UPI, Card
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('shop', 'invoice_number')

    def __str__(self):
        return self.invoice_number

    def get_total_cost(self):
        return self.total_amount - self.total_profit

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Sold price
    profit = models.DecimalField(max_digits=10, decimal_places=2) # Profit amount

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.product.name}"
