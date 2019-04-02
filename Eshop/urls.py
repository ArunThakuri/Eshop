"""Eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.urls import path
# from django.contrib import admin
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from cms.views import SignUpView
from shop.views import HomePage, ProductView, CartView, ProductsView, CategoryView, SearchView, CategoryApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='Homepage'),
    path('product/<int:product_id>', ProductView.as_view(), name='single_product_page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup', SignUpView.as_view(), name='signup'),
    path('cart/<int:product_id>', CartView.as_view(), name='cart_page'),
    path('products/', ProductsView.as_view(), name='products'),
    path('categories/<int:category_id>', CategoryView.as_view(), name='products'),
    path('search/', SearchView.as_view(), name='search'),
    path('api/categories', CategoryApi.as_view())
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
