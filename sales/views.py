from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from inventory.models import Shop, Product
from inventory.views import login_required_custom
from .models import Invoice, InvoiceItem

@login_required_custom
def billing_screen(request):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    
    
    if 'cart' not in request.session:
        request.session['cart'] = {}
        
    cart = request.session.get('cart', {})
    
   
    cart_total = 0.0
    for product_id, item in cart.items():
        cart_total += float(item['total'])
        
 
    search_id = request.GET.get('search_id', '')
    searched_product = None
    if search_id:
        search_id = search_id.strip()
        searched_product = Product.objects.filter(shop=shop, product_id__iexact=search_id).first()
        if not searched_product:
            messages.error(request, f"No product found with ID: {search_id}")
            
    context = {
        'shop': shop,
        'cart': cart,
        'cart_total': cart_total,
        'searched_product': searched_product,
        'search_id': search_id
    }
    return render(request, 'billing.html', context)

@login_required_custom
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        qty_str = request.POST.get('qty', '1')
        
        if not product_id:
            messages.error(request, "Product ID is missing.")
            return redirect('billing_screen')
            
        try:
            qty = int(qty_str)
            if qty <= 0:
                messages.error(request, "Quantity must be greater than zero.")
                return redirect('billing_screen')
        except ValueError:
            messages.error(request, "Invalid quantity.")
            return redirect('billing_screen')
            
        shop_id = request.session.get('shop_id')
        shop = Shop.objects.get(id=shop_id)
        product = get_object_or_404(Product, shop=shop, product_id=product_id)
        
        #chk stk lmit
        cart = request.session.get('cart', {})
        existing_qty = 0
        if product_id in cart:
            existing_qty = cart[product_id]['qty']
            
        new_qty = existing_qty + qty
        if new_qty > product.qty:
            messages.error(request, f"Insufficient stock for {product.name}. Available: {product.qty}, Already in bill: {existing_qty}.")
            return redirect('billing_screen')
            
        # updatecart
        cart[product_id] = {
            'name': product.name,
            'price': float(product.selling_price),
            'qty': new_qty,
            'total': float(product.selling_price * new_qty)
        }
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f"Added {product.name} (x{qty}) to bill.")
        
    return redirect('billing_screen')

@login_required_custom
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        item_name = cart[product_id]['name']
        del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f"Removed {item_name} from bill.")
    return redirect('billing_screen')

@login_required_custom
def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    messages.success(request, "Bill items cleared.")
    return redirect('billing_screen')

@login_required_custom
def checkout(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        payment_method = request.POST.get('payment_method')
        
        shop_id = request.session.get('shop_id')
        shop = Shop.objects.get(id=shop_id)
        
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Cannot checkout: Bill items list is empty.")
            return redirect('billing_screen')
            
        if not customer_name:
            customer_name = "Walking Customer"
            
        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return redirect('billing_screen')
            
     
        last_invoice = Invoice.objects.filter(shop=shop).order_by('id').last()
        if not last_invoice:
            new_inv_num = "INV-000001"
        else:
            last_num = last_invoice.invoice_number
            try:
                num_part = last_num.split('-')[1]
                next_num = int(num_part) + 1
                new_inv_num = f"INV-{next_num:06d}"
            except:
                new_inv_num = "INV-000001"
                
        
        invoice = Invoice(
            shop=shop,
            invoice_number=new_inv_num,
            customer_name=customer_name,
            payment_method=payment_method,
            total_amount=Decimal('0.0'),
            total_profit=Decimal('0.0')
        )
        invoice.save()
        
        invoice_total = Decimal('0.0')
        invoice_profit = Decimal('0.0')
        
   
        for product_id, item in cart.items():
            product = Product.objects.filter(shop=shop, product_id=product_id).first()
            if not product:
                messages.error(request, f"Product {item['name']} no longer exists.")
                invoice.delete()
                return redirect('billing_screen')
                
            qty = item['qty']
            if qty > product.qty:
                messages.error(request, f"Product {product.name} ran out of stock! Available: {product.qty}.")
                invoice.delete()
                return redirect('billing_screen')
                
            
            item_price = product.selling_price
            item_cost = product.purchase_price
            item_total = item_price * qty
            item_profit = (item_price - item_cost) * qty
            
            invoice_total += item_total
            invoice_profit += item_profit
            
           
            inv_item = InvoiceItem(
                invoice=invoice,
                product=product,
                qty=qty,
                price=item_price,
                profit=item_profit
            )
            inv_item.save()
            
           
            product.qty -= qty
            product.save()
            
     
        invoice.total_amount = invoice_total
        invoice.total_profit = invoice_profit
        invoice.save()
        
        
        request.session['cart'] = {}
        request.session.modified = True
        
        messages.success(request, f"Invoice {new_inv_num} generated successfully!")
        return redirect('invoice_detail', invoice_number=new_inv_num)
        
    return redirect('billing_screen')

@login_required_custom
def invoice_detail(request, invoice_number):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    invoice = get_object_or_404(Invoice, shop=shop, invoice_number=invoice_number)
    items = InvoiceItem.objects.filter(invoice=invoice).select_related('product')
    
    context = {
        'shop': shop,
        'invoice': invoice,
        'items': items
    }
    return render(request, 'invoice_detail.html', context)

@login_required_custom
def invoice_print(request, invoice_number):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    invoice = get_object_or_404(Invoice, shop=shop, invoice_number=invoice_number)
    items = InvoiceItem.objects.filter(invoice=invoice).select_related('product')
    
    context = {
        'shop': shop,
        'invoice': invoice,
        'items': items
    }
    return render(request, 'invoice_print.html', context)

@login_required_custom
def sales_history(request):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    
  
    invoices = Invoice.objects.filter(shop=shop).order_by('-date')
    
   
    grand_total_sales = 0.0
    grand_total_profits = 0.0
    for inv in invoices:
        grand_total_sales += float(inv.total_amount)
        grand_total_profits += float(inv.total_profit)
        
    context = {
        'shop': shop,
        'invoices': invoices,
        'grand_total_sales': grand_total_sales,
        'grand_total_profits': grand_total_profits
    }
    return render(request, 'sales_history.html', context)
