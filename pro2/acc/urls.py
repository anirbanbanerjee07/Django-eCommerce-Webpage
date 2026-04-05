from django.urls import path
from .import views

urlpatterns=[
    #login & registration
    path('login',views.loginpage,name='login'),
    path('registration',views.registration,name='registration'),
    path('logout',views.logoutpage,name='logout'),
    
    #server operations:
    path('',views.home,name='home'),
    path('tag/',views.tag_list,name='tag'),
    
    #dashboard operations:
    path('product',views.products,name='product'),
    path('customer/<int:pk_test>/',views.customer,name='customer'),
    path('customers/',views.customers,name='customers'),
    path('image/',views.image,name='image'),
    path('create_order/', views.select_customer_for_order, name='create_order'),
    path('create_order/<int:pk>/', views.createOrder, name='create_order_customer'),
    path('update_order/<int:pk>/', views.updateorder, name='update_order'),
    path('delete_order/<int:pk>/', views.deleteorder, name='delete_order'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_pending/', views.order_pending, name='order_pending'),
    path('delivered_orders/', views.delivered_orders, name='delivered_orders'),
    path('out_for_delivery/', views.out_for_delivery, name='out_for_delivery'),

    #customer operations:
    path('create_customer/', views.createCustomer, name='create_customer'),
    path('update_customer/<int:pk>/', views.updateCustomer, name='update_customer'),
    path('delete_customer/<int:pk>/', views.deleteCustomer, name='delete_customer'),
    path('customer_list',views.Customer_list,name='customer_list'),
    path('place_order/<int:pk>/',views.placeorder,name='place_order'),

    #product operation:
    path('add_product/', views.addProduct, name='add_product'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('delete_product/<int:pk>/', views.deleteProduct, name='delete_product'),
    
    #tag operations:
    path('import_tag',views.importtag,name='import_tag')

]