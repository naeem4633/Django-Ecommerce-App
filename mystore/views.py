from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from .models import Product, Cart, CartItem, Order
from django.urls import reverse_lazy
from .forms import AddToCartForm
from django.shortcuts import redirect
from decimal import Decimal
from django.http import HttpResponse


# Create your views here.

class IndexView(ListView):
    queryset = Product.objects.all()
    template_name = 'mystore/index.html'
    context_object_name = 'products'

    def post(self, request):
        if 'search_form' in self.request.POST:
            query = request.POST.get('q')
            if query:
                products = Product.objects.filter(name__icontains=query)
            else:
                products = None

            return render(request, 'mystore/index.html', {'filtered_products': products})
        
        elif 'filter_form' in self.request.POST:
            selected_option = self.request.POST.get('sort-by')
            if selected_option == 'high_to_low':
                products = Product.objects.all().order_by('-price')
            elif selected_option == 'low_to_high':
                products = Product.objects.all().order_by('price')
       
            return render(request, 'mystore/index.html', {'sorted_products': products})
        

class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = 'mystore/detail.html'
    form_class = AddToCartForm

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            product = self.get_object()
            quantity = form.cleaned_data['quantity']
            cart_id = request.session.get('cart_id')

            if request.POST.get('action') == 'cart':
                if cart_id:
                    try:
                        cart = Cart.objects.get(id=cart_id)
                        cart_item = CartItem.objects.get(cart=cart, product=product)
                        cart_item.quantity += quantity
                        cart_item.save()
                    except CartItem.DoesNotExist:
                        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
                else:
                    cart = Cart.objects.create()
                    request.session['cart_id'] = cart.id
                    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
                return redirect('cart')
            
            elif request.POST.get('action') == 'wishlist':
                if cart_id:
                    try:
                        cart = Cart.objects.get(id=cart_id)
                        cart_item = CartItem.objects.get(cart=cart, product=product)
                    except CartItem.DoesNotExist:
                        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=0) 
                    cart_item.is_wishlist_item = True
                    cart_item.save()    
                else:
                    cart = Cart.objects.create()
                    request.session['cart_id'] = cart.id
                    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=0, is_wishlist_item=True)
                    
            return redirect('wishlist')
        else:
            return self.form_invalid(form)


class CartItemList(ListView):
    model = CartItem
    template_name = 'mystore/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(quantity__gt=0)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items_to_include = CartItem.objects.filter(quantity__gt=0)
        total_price = sum((item.product.price * item.quantity) for item in items_to_include)
        context['total_price'] = total_price
        return context

    def get_success_url(self):
        return reverse_lazy('cart')
    
    def post(self, request):
        cart_item_id = self.request.POST.get('cart_item_id')
        new_quantity = self.request.POST.get('quantity')
        # total_price_str = self.request.POST.get('total_price')
        
        cart_item = CartItem.objects.get(id=cart_item_id)
        if cart_item.quantity > 0 and int(new_quantity) != 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.quantity = 0
            cart_item.save()
        # if cart_item.quantity < new_quantity:
        #     total_price = Decimal(total_price_str) + cart_item.product.price 
        # else:
        #     total_price = Decimal(total_price_str) - cart_item.product.price
            # total_price = Decimal(total_price_str) - cart_item.product.price

        return redirect('cart')

class WishlistView(ListView):
    model = CartItem
    template_name = 'mystore/wishlist.html'
    context_object_name = 'wishlist_items'

    def post(self, request):
        cart_item_id = self.request.POST.get('wishlist_item_id')
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.is_wishlist_item = False
        cart_item.save()
        if cart_item.quantity == 0:
            cart_item.delete()
        return redirect('wishlist')

    def get_queryset(self):
        return CartItem.objects.filter(is_wishlist_item=True)
    
class OrderPageView(ListView):
    model = Order
    template_name = 'mystore/order.html'
    context_object_name = 'order_items'

    def get_queryset(self):
        return Order.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = CartItem.objects.filter(quantity__gt=0)
        order_items = []
        for cart_item in cart_items:
            order_item = Order.objects.create(cartItem=cart_item, order_status="Processing")
            order_items.append(order_item)
        context['order_items'] = order_items
        return context
    
class OrderPageView(ListView):
    model = Order
    template_name = 'mystore/order.html'
    context_object_name = 'order_items'

    def get_queryset(self):
        return Order.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = CartItem.objects.filter(quantity__gt=0)
        order_items = []
        for cart_item in cart_items:
            order_item = Order.objects.create(cartItem=cart_item, order_status="Processing")
            order_items.append(order_item)
        context['order_items'] = order_items
        return context