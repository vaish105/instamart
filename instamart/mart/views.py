from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category

def home(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    
    return render(request, 'mart/home.html', {
        'products': products,
        'categories': categories
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('/')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for pid_str, qty in cart.items():
        pid = int(pid_str)
        product = get_object_or_404(Product, id=pid)
        subtotal = product.price * qty
        cart_items.append({
            'product': product,
            'qty': qty,
            'subtotal': subtotal
        })
        total += subtotal

    return render(request, 'mart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('view_cart')
