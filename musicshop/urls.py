from .views import *
from django.urls import path


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>', ProductsByCategory.as_view(), name='category'),
    path('search/', Search.as_view(), name='search'),
    path('contact/', get_message, name='contact'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('product/<str:slug>', Product.as_view(), name='product'),

]