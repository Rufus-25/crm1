from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username
            )

            messages.success(request, "Account was created successfully for " + username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Wrong username or password")
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    order_total = orders.count()
    order_delivered = orders.filter(status="Delivered").count()
    order_pending = orders.filter(status="Pending").count()
    context = {'customers':customers, 'orders':orders, 'order_total':order_total, 
    'order_delivered':order_delivered, 'order_pending':order_pending}    
    return render(request, 'accounts/dashboard.html', context)

def user_page(request):
    orders = request.user.customer.order_set.all()
    order_total = orders.count()
    order_delivered = orders.filter(status="Delivered").count()
    order_pending = orders.filter(status="Pending").count()
    context = {'orders':orders, 'order_total':order_total, 
    'order_delivered':order_delivered, 'order_pending':order_pending}
    return render(request, 'accounts/user.html', context)

def profile(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {'form':form}
    return render(request, 'accounts/profile_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    customer_orders = customer.order_set.all()
    my_filter = OrderFilter(request.GET, queryset=customer_orders)
    customer_orders = my_filter.qs
    total_customer_order = customer_orders.count()
    context = {'customer':customer, 'customer_orders':customer_orders, 
    'total_customer_order':total_customer_order, 'my_filter':my_filter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    formset = OrderFormSet(instance=customer, queryset=Order.objects.none())
    #form = OrderForm()
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset, 'customer':customer}
    return render(request, 'accounts/create_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form, 'order':order}
    return render(request, 'accounts/update_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)
