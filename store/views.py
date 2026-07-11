from django.shortcuts import render, redirect
from .models import Product, Order , Category

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def home(request):

    query = request.GET.get('search')

    category = request.GET.get('category')

    products = Product.objects.all()

    if query:

        products = products.filter(name__icontains=query)

    if category:

        products = products.filter(category__name=category)

    categories = Category.objects.all()

    return render(request, 'index.html', {
        'products': products,
        'categories': categories
    })

def product_detail(request, id):

    product = Product.objects.get(id=id)

    return render(request, 'product_detail.html', {
        'product': product
    })


def add_to_cart(request, id):

    cart = request.session.get('cart', {})

    id = str(id)

    if id in cart:

        cart[id] += 1

    else:

        cart[id] = 1

    request.session['cart'] = cart

    return redirect('/cart/')

def cart(request):

    cart = request.session.get('cart')

    if cart is None:
        cart = {}

    ids = cart.keys()

    products = Product.objects.filter(id__in=ids)

    cart_items = []

    total = 0

    for product in products:

        quantity = cart[str(product.id)]

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():

            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        return redirect('/login/')

    return render(request, 'register.html')

def login_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

        else:

            return render(request, 'login.html', {
                'error': 'Invalid Username or Password'
            })

    return render(request, 'login.html')

def logout_user(request):

    logout(request)

    return redirect('/')

def checkout(request):

    if not request.user.is_authenticated:

        return redirect('/login/')


    cart = request.session.get('cart')

    if cart is None:
        cart = {}

    ids = cart.keys()

    products = Product.objects.filter(id__in=ids)

    total = 0

    for product in products:

        quantity = cart[str(product.id)]

        total += product.price * quantity


    if request.method == 'POST':

        address = request.POST['address']

        phone = request.POST['phone']


        order = Order.objects.create(
            user=request.user,
            total_price=total,
            address=address,
            phone=phone
        )


        order.products.set(products)

        request.session['cart'] = {}

        return redirect('/orders/')


    return render(request, 'checkout.html', {
        'products': products,
        'total': total
    })

def orders(request):

    if not request.user.is_authenticated:

        return redirect('/login/')


    user_orders = Order.objects.filter(user=request.user)

    return render(request, 'orders.html', {
        'orders': user_orders
    })

def remove_from_cart(request, id):

    cart = request.session.get('cart')

    if cart is None:
        cart = {}

    id = str(id)

    if id in cart:

        if cart[id] > 1:

            cart[id] -= 1

        else:

            del cart[id]

    request.session['cart'] = cart

    return redirect('/cart/')