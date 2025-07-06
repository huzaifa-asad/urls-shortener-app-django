from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.list_urls, name='list_urls'),
    path('delete/<int:pk>/', views.delete_url, name='delete_url'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('analytics/data/', views.analytics_chart_data, name='analytics_chart_data'),
    path('qr/<str:code>/', views.qr_code_page, name='qr_code_page'),
    path('qr/<str:code>/generate/', views.generate_qr_code, name='generate_qr_code'),
    path('qr/<str:code>/download/', views.download_qr_code, name='download_qr_code'),
    path('<str:code>/', views.redirect_short_url, name='redirect_short_url'),
]
