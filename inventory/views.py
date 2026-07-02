import qrcode
from io import BytesIO
from django.core.files import File
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Shop, Category, Subcategory, Product


def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if 'shop_id' not in request.session:
            messages.error(request, "Please log in first.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def signup(request):
    if request.method == 'POST':
        owner_name = request.POST.get('owner_name')
        shop_name = request.POST.get('shop_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        logo = request.FILES.get('logo')

        
        if not owner_name or not shop_name or not email or not password or not phone or not address:
            messages.error(request, "All fields are required!")
            return render(request, 'signup.html')

        if Shop.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return render(request, 'signup.html')

       
        hashed_password = make_password(password)
        shop = Shop(
            owner_name=owner_name,
            shop_name=shop_name,
            email=email,
            password=hashed_password,
            phone=phone,
            address=address,
            logo=logo
        )
        shop.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'login.html')

        shop = Shop.objects.filter(email=email).first()
        if shop and check_password(password, shop.password):
            # Loginsuccessful store shop_id in session
            request.session['shop_id'] = shop.id
            request.session['shop_name'] = shop.shop_name
            messages.success(request, f"Welcome back, {shop.shop_name}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        owner_name = request.POST.get('owner_name')
        new_password = request.POST.get('new_password')

        shop = Shop.objects.filter(email=email, phone=phone, owner_name=owner_name).first()
        if shop:
            shop.password = make_password(new_password)
            shop.save()
            messages.success(request, "Password reset successful! Please log in with your new password.")
            return redirect('login')
        else:
            messages.error(request, "No matching shop found with the provided details.")
            return render(request, 'forgot_password.html')

    return render(request, 'forgot_password.html')


@login_required_custom
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        shop_id = request.session.get('shop_id')
        shop = Shop.objects.get(id=shop_id)

        if not current_password or not new_password or not confirm_password:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'change_password.html')

        
        if not check_password(current_password, shop.password):
            messages.error(request, "Incorrect current password.")
            return render(request, 'change_password.html')

        
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return render(request, 'change_password.html')

       
        shop.password = make_password(new_password)
        shop.save()
        messages.success(request, "Password changed successfully!")
        return redirect('dashboard')

    return render(request, 'change_password.html')

@login_required_custom
def dashboard(request):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    context = {
        'shop': shop
    }
    return render(request, 'dashboard.html', context)


@login_required_custom
def categories_list(request):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            messages.error(request, "Category name is required.")
        else:
            name = name.strip()
            if Category.objects.filter(shop=shop, name__iexact=name).exists():
                messages.error(request, f"Category '{name}' already exists.")
            else:
                category = Category(shop=shop, name=name)
                category.save()
                messages.success(request, f"Category '{name}' added successfully.")
                return redirect('categories_list')
                
    categories = Category.objects.filter(shop=shop).order_by('name')
    context = {
        'shop': shop,
        'categories': categories
    }
    return render(request, 'categories.html', context)

@login_required_custom
def edit_category(request, category_id):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    category = get_object_or_404(Category, shop=shop, id=category_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            messages.error(request, "Category name cannot be empty.")
        else:
            name = name.strip()
            # Check if name exists in another category
            if Category.objects.filter(shop=shop, name__iexact=name).exclude(id=category.id).exists():
                messages.error(request, f"Category '{name}' already exists.")
            else:
                category.name = name
                category.save()
                messages.success(request, "Category updated successfully.")
                return redirect('categories_list')
                
    context = {
        'shop': shop,
        'category': category
    }
    return render(request, 'edit_category.html', context)

@login_required_custom
def delete_category(request, category_id):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    category = get_object_or_404(Category, shop=shop, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect('categories_list')



@login_required_custom
def subcategories_list(request):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        
        if not category_id or not name:
            messages.error(request, "All fields are required to add a subcategory.")
        else:
            name = name.strip()
            category = get_object_or_404(Category, shop=shop, id=category_id)
            if Subcategory.objects.filter(shop=shop, category=category, name__iexact=name).exists():
                messages.error(request, f"Subcategory '{name}' already exists in Category '{category.name}'.")
            else:
                subcategory = Subcategory(shop=shop, category=category, name=name)
                subcategory.save()
                messages.success(request, f"Subcategory '{name}' added successfully.")
                return redirect('subcategories_list')
                
    subcategories = Subcategory.objects.filter(shop=shop).select_related('category').order_by('category__name', 'name')
    categories = Category.objects.filter(shop=shop).order_by('name')
    context = {
        'shop': shop,
        'subcategories': subcategories,
        'categories': categories
    }
    return render(request, 'subcategories.html', context)

@login_required_custom
def edit_subcategory(request, subcategory_id):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    subcategory = get_object_or_404(Subcategory, shop=shop, id=subcategory_id)
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        
        if not category_id or not name:
            messages.error(request, "Fields cannot be empty.")
        else:
            name = name.strip()
            category = get_object_or_404(Category, shop=shop, id=category_id)
            if Subcategory.objects.filter(shop=shop, category=category, name__iexact=name).exclude(id=subcategory.id).exists():
                messages.error(request, f"Subcategory '{name}' already exists in Category '{category.name}'.")
            else:
                subcategory.category = category
                subcategory.name = name
                subcategory.save()
                messages.success(request, "Subcategory updated successfully.")
                return redirect('subcategories_list')
                
    categories = Category.objects.filter(shop=shop).order_by('name')
    context = {
        'shop': shop,
        'subcategory': subcategory,
        'categories': categories
    }
    return render(request, 'edit_subcategory.html', context)

@login_required_custom
def delete_subcategory(request, subcategory_id):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    subcategory = get_object_or_404(Subcategory, shop=shop, id=subcategory_id)
    subcategory.delete()
    messages.success(request, "Subcategory deleted successfully.")
    return redirect('subcategories_list')

#pr crud

@login_required_custom
def products_list(request):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    
    query = request.GET.get('q', '')
    if query:
        query = query.strip()
        products = Product.objects.filter(
            models.Q(shop=shop) & (
                models.Q(product_id__icontains=query) |
                models.Q(name__icontains=query) |
                models.Q(category__name__icontains=query)
            )
        ).select_related('category', 'subcategory').order_by('product_id')
    else:
        products = Product.objects.filter(shop=shop).select_related('category', 'subcategory').order_by('product_id')
        
   
    context = {
        'shop': shop,
        'products': products,
        'query': query,
        'low_stock_limit': 5
    }
    return render(request, 'products.html', context)

@login_required_custom
def add_product(request):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        name = request.POST.get('name')
        purchase_price = request.POST.get('purchase_price')
        selling_price = request.POST.get('selling_price')
        qty = request.POST.get('qty')
        rack_location = request.POST.get('rack_location')
        image = request.FILES.get('image')
        
        if not category_id or not subcategory_id or not name or not purchase_price or not selling_price or not qty or not rack_location:
            messages.error(request, "All fields are required to add a product.")
        else:
            category = get_object_or_404(Category, shop=shop, id=category_id)
            subcategory = get_object_or_404(Subcategory, shop=shop, id=subcategory_id)
            
            # 1. Automatic Product ID Generation (SAR-XXXXXX)
            last_product = Product.objects.filter(shop=shop).order_by('id').last()
            if not last_product:
                new_id = "SAR-000001"
            else:
                last_id = last_product.product_id
                try:
                    num_part = last_id.split('-')[1]
                    next_num = int(num_part) + 1
                    new_id = f"SAR-{next_num:06d}"
                except:
                    # Fallback if ID is in unexpected format
                    new_id = "SAR-000001"
            
            # Save product object first (without QR code) to get paths
            product = Product(
                shop=shop,
                product_id=new_id,
                category=category,
                subcategory=subcategory,
                name=name,
                purchase_price=purchase_price,
                selling_price=selling_price,
                qty=qty,
                rack_location=rack_location,
                image=image
            )
            product.save()
            
            #  qgreneration
            qr_content = f"Product ID: {product.product_id}\nName: {product.name}\nCategory: {product.category.name}\nSelling Price: Rs.{product.selling_price}\nStock: {product.qty}\nRack: {product.rack_location}"
            qr = qrcode.QRCode(version=1, box_size=5, border=3)
            qr.add_data(qr_content)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR to product model qr_code field
            buf = BytesIO()
            img.save(buf, format='PNG')
            qr_filename = f"qr_{product.product_id}.png"
            product.qr_code.save(qr_filename, File(buf), save=True)
            
            messages.success(request, f"Product {product.name} added successfully with ID {product.product_id}.")
            return redirect('products_list')
            
    categories = Category.objects.filter(shop=shop).order_by('name')
    subcategories = Subcategory.objects.filter(shop=shop).order_by('name')
    context = {
        'shop': shop,
        'categories': categories,
        'subcategories': subcategories
    }
    return render(request, 'add_product.html', context)

@login_required_custom
def edit_product(request, product_id):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    product = get_object_or_404(Product, shop=shop, product_id=product_id)
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        name = request.POST.get('name')
        purchase_price = request.POST.get('purchase_price')
        selling_price = request.POST.get('selling_price')
        qty = request.POST.get('qty')
        rack_location = request.POST.get('rack_location')
        image = request.FILES.get('image')
        
        if not category_id or not subcategory_id or not name or not purchase_price or not selling_price or not qty or not rack_location:
            messages.error(request, "All fields are required.")
        else:
            category = get_object_or_404(Category, shop=shop, id=category_id)
            subcategory = get_object_or_404(Subcategory, shop=shop, id=subcategory_id)
            
            product.category = category
            product.subcategory = subcategory
            product.name = name
            product.purchase_price = purchase_price
            product.selling_price = selling_price
            product.qty = qty
            product.rack_location = rack_location
            
            if image:
                product.image = image
                
            product.save()
            
            qr_content = f"Product ID: {product.product_id}\nName: {product.name}\nCategory: {product.category.name}\nSelling Price: Rs.{product.selling_price}\nStock: {product.qty}\nRack: {product.rack_location}"
            qr = qrcode.QRCode(version=1, box_size=5, border=3)
            qr.add_data(qr_content)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buf = BytesIO()
            img.save(buf, format='PNG')
            qr_filename = f"qr_{product.product_id}.png"
            product.qr_code.save(qr_filename, File(buf), save=True)
            
            messages.success(request, "Product updated successfully.")
            return redirect('products_list')
            
    categories = Category.objects.filter(shop=shop).order_by('name')
    subcategories = Subcategory.objects.filter(shop=shop).order_by('name')
    context = {
        'shop': shop,
        'product': product,
        'categories': categories,
        'subcategories': subcategories
    }
    return render(request, 'edit_product.html', context)

@login_required_custom
def delete_product(request, product_id):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    product = get_object_or_404(Product, shop=shop, product_id=product_id)
  
    if product.image:
        product.image.delete(save=False)
    if product.qr_code:
        product.qr_code.delete(save=False)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('products_list')

@login_required_custom
def product_details(request, product_id):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    product = get_object_or_404(Product, shop=shop, product_id=product_id)
    context = {
        'shop': shop,
        'product': product
    }
    return render(request, 'product_details.html', context)
