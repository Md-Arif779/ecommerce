from django.urls import path
from users import views


urlpatterns = [
   path('signup/', views.register, name = "signup"),
   path('signin/', views.login, name = "signin"),
   path('logout/', views.logout, name = "logout"),
]