from django.urls import path
from . import views
from core.views import download_allocations_pdf

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('teachers/<int:pk>/edit/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),
    path('disciplines/', views.discipline_list, name='discipline_list'),
    path('disciplines/add/', views.discipline_create, name='discipline_create'),
    path('disciplines/<int:pk>/', views.discipline_detail, name='discipline_detail'),
    path('disciplines/<int:pk>/edit/', views.discipline_update, name='discipline_update'),
    path('disciplines/<int:pk>/delete/', views.discipline_delete, name='discipline_delete'),
    path('spaces/', views.space_list, name='space_list'),
    path('spaces/add/', views.space_create, name='space_create'),
    path('spaces/<int:pk>/', views.space_detail, name='space_detail'),
    path('spaces/<int:pk>/edit/', views.space_update, name='space_update'),
    path('spaces/<int:pk>/delete/', views.space_delete, name='space_delete'),
    path('allocations/', views.allocation_list, name='allocation_list'),
    path('allocations/add/', views.allocation_create, name='allocation_create'),
    path('allocations/<int:pk>/', views.allocation_detail, name='allocation_detail'),
    path('allocations/<int:pk>/edit/', views.allocation_update, name='allocation_update'),
    path('allocations/<int:pk>/delete/', views.allocation_delete, name='allocation_delete'),
    path('allocations/generate_ensalamento/', views.generate_ensalamento, name='generate_ensalamento'),
    path('allocations/download/pdf/', download_allocations_pdf, name='download_allocations_pdf'),
]
