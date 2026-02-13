from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),               
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('packages/', views.packages, name='packages'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('book/<int:package_id>/', views.book_now, name='book_now'),



    
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-add-package/', views.admin_add_package, name='admin_add_package'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),


]
