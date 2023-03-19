from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('asset-list/', views.asset_list, name='asset-list'),
    path('asset-detail/<str:pk>/', views.asset_detail, name='asset-detail'),
    path('asset-create/', views.asset_create, name='asset-create'),
    path('asset-update/<str:pk>', views.asset_update, name='asset-update'),
    path('asset-update-all/', views.asset_update_all, name='asset-update-all'),
    path('asset-delete/<str:pk>', views.asset_delete, name='asset-delete')
]