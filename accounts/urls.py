from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name="register"),
    path('login', views.loginPage, name="login"),
    path('logout', views.logoutPage, name="logout"),

    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>', views.customer, name="customer"),
    path('user', views.user_page, name="user-page"),
    path('profile', views.profile, name="profile"),
    
    path('create_order/<str:pk>', views.create_order, name="create_order"),
    path('update_order/<str:pk>', views.update_order, name="update_order"),
    path('delete_order/<str:pk>', views.delete_order, name="delete_order"),
    

]