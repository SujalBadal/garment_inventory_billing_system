from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal
import datetime
from inventory.models import Shop, Product
from sales.models import Invoice, InvoiceItem
from inventory.views import login_required_custom

@login_required_custom
def reports_dashboard(request):
    shop_id = request.session.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    
    total_products = Product.objects.filter(shop=shop).count()
    
   
    total_stock = Product.objects.filter(shop=shop).aggregate(sum_stock=Sum('qty'))['sum_stock'] or 0
    
    
    today = timezone.localtime(timezone.now()).date()
    
  
    today_invoices = Invoice.objects.filter(shop=shop, date__date=today)
    today_sales = today_invoices.aggregate(sum_sales=Sum('total_amount'))['sum_sales'] or Decimal('0.0')
    today_profit = today_invoices.aggregate(sum_profit=Sum('total_profit'))['sum_profit'] or Decimal('0.0')
    
    
    low_stock_products = Product.objects.filter(shop=shop, qty__lte=5).select_related('category').order_by('qty')
    
   
    best_sellers = InvoiceItem.objects.filter(invoice__shop=shop).values(
        'product__product_id', 
        'product__name', 
        'product__selling_price'
    ).annotate(
        total_sold=Sum('qty')
    ).order_by('-total_sold')[:5]
    
    recent_sales = Invoice.objects.filter(shop=shop).order_by('-date')[:5]
    
    daily_date_str = request.GET.get('daily_date', '')
    if daily_date_str:
        try:
            daily_date = datetime.datetime.strptime(daily_date_str, '%Y-%m-%d').date()
        except ValueError:
            daily_date = today
    else:
        daily_date = today
        
    daily_invoices = Invoice.objects.filter(shop=shop, date__date=daily_date).order_by('-date')
    daily_sales_total = daily_invoices.aggregate(sum_sales=Sum('total_amount'))['sum_sales'] or Decimal('0.0')
    daily_profit_total = daily_invoices.aggregate(sum_profit=Sum('total_profit'))['sum_profit'] or Decimal('0.0')
   
    weekly_reports = []
    for i in range(4):
        start_day = today - datetime.timedelta(days=(i+1)*7 - 1)
        end_day = today - datetime.timedelta(days=i*7)
        week_invoices = Invoice.objects.filter(shop=shop, date__date__range=[start_day, end_day])
        w_sales = week_invoices.aggregate(sum_sales=Sum('total_amount'))['sum_sales'] or Decimal('0.0')
        w_profit = week_invoices.aggregate(sum_profit=Sum('total_profit'))['sum_profit'] or Decimal('0.0')
        weekly_reports.append({
            'label': f"Week {i+1} ({start_day.strftime('%d %b')} to {end_day.strftime('%d %b')})",
            'sales': w_sales,
            'profit': w_profit,
            'invoice_count': week_invoices.count()
        })
        
   
    monthly_month_str = request.GET.get('monthly_month', '')
    monthly_year_str = request.GET.get('monthly_year', '')
    
    if monthly_month_str and monthly_year_str:
        try:
            monthly_month = int(monthly_month_str)
            monthly_year = int(monthly_year_str)
        except ValueError:
            monthly_month = today.month
            monthly_year = today.year
    else:
        monthly_month = today.month
        monthly_year = today.year
        
    monthly_invoices = Invoice.objects.filter(shop=shop, date__year=monthly_year, date__month=monthly_month).order_by('-date')
    monthly_sales_total = monthly_invoices.aggregate(sum_sales=Sum('total_amount'))['sum_sales'] or Decimal('0.0')
    monthly_profit_total = monthly_invoices.aggregate(sum_profit=Sum('total_profit'))['sum_profit'] or Decimal('0.0')
    
 
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')
    
    custom_invoices = []
    custom_sales_total = Decimal('0.0')
    custom_profit_total = Decimal('0.0')
    custom_cost_total = Decimal('0.0')
    
    if start_date_str and end_date_str:
        try:
            start_dt = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_dt = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            start_dt = today - datetime.timedelta(days=30)
            end_dt = today
            start_date_str = start_dt.strftime('%Y-%m-%d')
            end_date_str = end_dt.strftime('%Y-%m-%d')
            
        custom_invoices = Invoice.objects.filter(shop=shop, date__date__range=[start_dt, end_dt]).order_by('-date')
        custom_sales_total = custom_invoices.aggregate(sum_sales=Sum('total_amount'))['sum_sales'] or Decimal('0.0')
        custom_profit_total = custom_invoices.aggregate(sum_profit=Sum('total_profit'))['sum_profit'] or Decimal('0.0')
        custom_cost_total = custom_sales_total - custom_profit_total
    else:
       
        start_dt = today - datetime.timedelta(days=30)
        end_dt = today
        start_date_str = start_dt.strftime('%Y-%m-%d')
        end_date_str = end_dt.strftime('%Y-%m-%d')
        
        custom_invoices = Invoice.objects.filter(shop=shop, date__date__range=[start_dt, end_dt]).order_by('-date')
        custom_sales_total = custom_invoices.aggregate(sum_sales=Sum('total_amount'))['sum_sales'] or Decimal('0.0')
        custom_profit_total = custom_invoices.aggregate(sum_profit=Sum('total_profit'))['sum_profit'] or Decimal('0.0')
        custom_cost_total = custom_sales_total - custom_profit_total
        
    
    year_choices = range(today.year - 5, today.year + 1)
    month_choices = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    context = {
        'shop': shop,
        'total_products': total_products,
        'total_stock': total_stock,
        'today_sales': today_sales,
        'today_profit': today_profit,
        'low_stock_products': low_stock_products,
        'best_sellers': best_sellers,
        'recent_sales': recent_sales,
        
      
        'daily_date': daily_date.strftime('%Y-%m-%d'),
        'daily_invoices': daily_invoices,
        'daily_sales_total': daily_sales_total,
        'daily_profit_total': daily_profit_total,
        
        'weekly_reports': weekly_reports,
        
        'monthly_month': monthly_month,
        'monthly_year': monthly_year,
        'monthly_invoices': monthly_invoices,
        'monthly_sales_total': monthly_sales_total,
        'monthly_profit_total': monthly_profit_total,
        'year_choices': year_choices,
        'month_choices': month_choices,
        
        # Custom Profit Report
        'start_date': start_date_str,
        'end_date': end_date_str,
        'custom_invoices': custom_invoices,
        'custom_sales_total': custom_sales_total,
        'custom_profit_total': custom_profit_total,
        'custom_cost_total': custom_cost_total
    }
    
    return render(request, 'reports_dashboard.html', context)
