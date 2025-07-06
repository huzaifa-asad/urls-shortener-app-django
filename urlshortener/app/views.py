from django.shortcuts import render, get_object_or_404, redirect
from .models import URL
from .forms import UserRegisterForm, URLForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .utils import generate_short_code
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from datetime import timedelta
from django.utils import timezone
import qrcode

# Create your views here.

def home(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url_obj = form.save(commit=False)
            url_obj.user = request.user if request.user.is_authenticated else None
            url_obj.short_code = generate_short_code()
            url_obj.save()
            return render(request, 'success.html', {
                'short_code': url_obj.short_code,
                'url_obj': url_obj
            })
    else:
        form = URLForm()
    return render(request, 'home.html', {'form': form})


# Redirect the short URL.
def redirect_short_url(request, code):
    url_obj = get_object_or_404(URL, short_code=code)
    url_obj.clicks += 1
    url_obj.save()
    return redirect(url_obj.original_url)

# List all URLs
@login_required
def list_urls(request):
    urls = URL.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'list.html', {'urls': urls})

# Delete a short URL
@login_required
def delete_url(request, pk):
    url_obj = get_object_or_404(URL, pk=pk)
    url_obj.delete()
    return redirect('list_urls')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log them in automatically after registration
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

# Analytics Dashboard
@login_required
def analytics_dashboard(request):
    user_urls = URL.objects.filter(user=request.user) if request.user.is_authenticated else URL.objects.none()
    
    # Basic statistics
    total_urls = user_urls.count()
    total_clicks = user_urls.aggregate(Sum('clicks'))['clicks__sum'] or 0
    
    # Top 5 most clicked URLs
    top_urls = user_urls.order_by('-clicks')[:5]
    
    # Recent URLs (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_urls = user_urls.filter(created_at__gte=seven_days_ago)
    
    context = {
        'total_urls': total_urls,
        'total_clicks': total_clicks,
        'top_urls': top_urls,
        'recent_urls_count': recent_urls.count(),
    }
    
    return render(request, 'analytics.html', context)

# API endpoint for chart data
@login_required
def analytics_chart_data(request):
    user_urls = URL.objects.filter(user=request.user) if request.user.is_authenticated else URL.objects.none()
    
    # Daily clicks data for the last 7 days
    daily_data = []
    for i in range(7):
        date = timezone.now().date() - timedelta(days=i)
        # For simplicity, we'll use creation date as proxy for click date
        # In a real app, you'd want a separate ClickLog model
        urls_created = user_urls.filter(created_at__date=date)
        total_clicks = urls_created.aggregate(Sum('clicks'))['clicks__sum'] or 0
        daily_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'clicks': total_clicks
        })
    
    daily_data.reverse()  # Show oldest first
    
    # Top URLs data for pie chart
    top_urls_data = []
    top_urls = user_urls.order_by('-clicks')[:5]
    for url in top_urls:
        top_urls_data.append({
            'short_code': url.short_code,
            'clicks': url.clicks,
            'original_url': url.original_url[:30] + '...' if len(url.original_url) > 30 else url.original_url
        })
    
    # URLs created per day (last 7 days)
    creation_data = []
    for i in range(7):
        date = timezone.now().date() - timedelta(days=i)
        count = user_urls.filter(created_at__date=date).count()
        creation_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    creation_data.reverse()
    
    return JsonResponse({
        'daily_clicks': daily_data,
        'top_urls': top_urls_data,
        'url_creation': creation_data
    })

# QR Code views
def generate_qr_code(request, code):
    """Generate and return QR code image for the original URL"""
    url_obj = get_object_or_404(URL, short_code=code)
    
    # Use the original URL directly
    target_url = url_obj.original_url
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(target_url)
    qr.make(fit=True)
    
    # Create image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Return image as HTTP response
    response = HttpResponse(content_type="image/png")
    qr_image.save(response, "PNG")
    return response

def download_qr_code(request, code):
    """Download QR code as PNG file"""
    url_obj = get_object_or_404(URL, short_code=code)
    
    # Use the original URL directly
    target_url = url_obj.original_url
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(target_url)
    qr.make(fit=True)
    
    # Create image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Return as downloadable file
    response = HttpResponse(content_type="image/png")
    response['Content-Disposition'] = f'attachment; filename="{code}_qr_code.png"'
    qr_image.save(response, "PNG")
    return response

@login_required
def qr_code_page(request, code):
    """Display QR code page for a specific URL"""
    url_obj = get_object_or_404(URL, short_code=code)
    
    # Check if user owns this URL
    if url_obj.user != request.user:
        messages.error(request, 'You do not have permission to view this QR code.')
        return redirect('list_urls')
    
    context = {
        'url': url_obj,
        'qr_code_data_url': url_obj.get_qr_code_data_url(request),
        'short_url': url_obj.get_short_url(request)
    }
    return render(request, 'qr_code.html', context)
