from django.urls import path
from .views import (
    CustomerListView, 
    CustomerDetailView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
    ajax_add_activity
)


urlpatterns = [
    path('', CustomerListView.as_view(), name="customer_list"),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name="customer_detail"),
    path('customer/new/', CustomerCreateView.as_view(), name='customer_create'),
    path('customer/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('ajax/add_activity/', ajax_add_activity, name='ajax_add_activity'),
]
