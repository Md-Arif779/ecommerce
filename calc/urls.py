
from django.urls import path
from .import views


urlpatterns = [
   path('', views.home, name = "home"),
   path('products/', views.product_list, name = "products"),
   path('product-detail/<pid>/', views.product_detail, name = "product-detail"),

   path('categorys/', views.category_list, name = "categorys"),
   path('categorys-product-list/<cid>/', views.category_product_list, name = "categorys-product-list"),

   path('vendor/', views.vendor, name = "vendor"),
   path('vendor-detail/<vid>/', views.vendor_detail, name = "vendor-detail"),   

   path('product/tags/<slug:tag_slug>/', views.tag_list, name = "tags"), 

   # Add Search
   path('search/', views.search, name = "search"),
  

]