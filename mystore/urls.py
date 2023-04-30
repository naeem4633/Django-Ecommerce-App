from django.urls import include, path
from .views import IndexView, ProductDetailView, CartItemList, WishlistView, OrderPageView
from . import views

appname = 'mystore'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('cart', CartItemList.as_view(), name='cart'),
    path('wishlist', WishlistView.as_view(), name='wishlist'),
    path('order', OrderPageView.as_view(), name='order'),
]