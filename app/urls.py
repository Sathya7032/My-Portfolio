from django.urls import path
# pyrefly: ignore [missing-import]
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),

    # Neo-Brutalist Admin Dashboard Routes
    path('dashboard/', views.dashboard_index, name='dashboard_index'),
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
    path('dashboard/blogs/', views.dashboard_blogs, name='dashboard_blogs'),
    path('dashboard/blogs/create/', views.dashboard_blog_create, name='dashboard_blog_create'),
    path('dashboard/blogs/<int:pk>/edit/', views.dashboard_blog_edit, name='dashboard_blog_edit'),
    path('dashboard/blogs/<int:pk>/toggle/', views.dashboard_blog_toggle, name='dashboard_blog_toggle'),
    path('dashboard/blogs/<int:pk>/delete/', views.dashboard_blog_delete, name='dashboard_blog_delete'),
    path('dashboard/messages/', views.dashboard_messages, name='dashboard_messages'),
    path('dashboard/messages/<int:pk>/toggle/', views.dashboard_message_toggle, name='dashboard_message_toggle'),
    path('dashboard/messages/<int:pk>/delete/', views.dashboard_message_delete, name='dashboard_message_delete'),
]