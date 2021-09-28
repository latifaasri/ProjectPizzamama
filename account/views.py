from django.shortcuts import render, redirect
from django.forms import inlineformset_factory  # to make a multi_forms fields
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth.forms import UserCreationForm
# that is for showing message if you loging in this work
from django.contrib import messages
# that is specially for checking user and login/out
from django.contrib.auth import authenticate, login, logout
# decorator in python allow us to applicate a function in another function
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group


@unauthenticated_user
def registerpage(request):
    form = CreateUserform
    if request.method == 'POST':
        form = CreateUserform(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # every account created is a customer user
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(
                request, 'you have successfully registred ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)


@unauthenticated_user
def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.info(
                request, 'Username or password is incorrect. Try again')
    context = {}
    return render(request, 'login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS:', orders)

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'userpage.html', context)


# only who is login can see home page otherwise redirect to login page
@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_oders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {'orders': orders, 'customers': customers, 'total_customers': total_customers,
               'total_orders': total_oders, 'delivered': delivered, 'pending': pending}
    return render(request, "Home.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'settings_user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, "product.html", {"products": products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    myfilter = Orderfilter(request.GET, queryset=orders)
    orders = myfilter.qs
    context = {'customer': customer, 'orders': orders,
               'total_orders': total_orders, 'myfilter': myfilter}
    return render(request, "customer.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createorder(request, pk):
    SetOrder = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    form = SetOrder(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})# for one customer
    if request.method == 'POST':
        form = SetOrder(request.POST, instance=customer)
        # form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"form": form}
    return render(request, "orderform.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateorder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, "orderform.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteorder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, "deleteorder.html", context)
