"""eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import main.views as shop

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', shop.index, name='store'),
    path('register/', shop.registerPage, name = 'register'),
    path('login/', shop.loginPage, name = 'login'),
    path('logout/', shop.logoutUser, name='logout'),
    path('cart/', shop.cart, name='cart'),
    path('checkout/', shop.checkout, name='checkout'),
    path('update_item/', shop.updateItem, name='updateItem'),
    path('process_order/', shop.processOrder, name='processOrder'),
    path('roast/', shop.roast),
    path('flavor/', shop.flavor),
    path('flavor_detail/', shop.flavor_detail),
    path('<int:beanno>/', shop.bean_detail, name='beans-url'),
    path('/roast/<str:rtype>/', shop.shop_roast, name='roast-url'),
    path('/flavor/<str:ftype>/', shop.shop_flavor, name='flavor-url'),
]

