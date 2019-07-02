from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .forms import *
import datetime
from django.contrib.auth import authenticate, login, logout
from myapp.forms import SignUpForm
from django.contrib.auth.decorators import login_required

#Create your views

#signup custom view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('myapp:index')

    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})

#user login(initial)
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                current_login_time = str(datetime.datetime.now())
                # session parameter last_login
                request.session['last_login'] = current_login_time
                request.session.set_expiry(3600)
                request.session['username']=username
                # set session expiry to 1 hour
                login(request,user)
                return render(request,'myapp/index.html', {'username':username})
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

#user_logout method
@login_required
def user_logout(request):
    logout(request)
    return render(request,'myapp/login.html')

#index method
@login_required
def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    #request.COOKIES['about_visits']=0
    #request.set_cookie('about_visits', expire=datetime.time(00, 5, 00))
    return render(request,'myapp/index.html',{'cat_list':cat_list})

#about method
def about(request):
    if request.session.has_key('username'):
        cookievalue = request.COOKIES.get('about_visits', 'default')
        if (cookievalue == 'default'):
            response = render(request, 'myapp/about.html', {'about_visits': '1'})
            response.set_cookie('about_visits', 1, 5 * 60)
            return response
        else:
            cookievalue = int(cookievalue) + 1
            response = render(request, 'myapp/about.html', {'about_visits': cookievalue})
            response.set_cookie('about_visits', cookievalue)
            return response
    else:
        return redirect('/myapp/login')

#detail method
@login_required
def detail(request,cat_no):
    response = HttpResponse()
    cat_list = get_object_or_404(Category, id=cat_no)
    response.write('<h3>' + 'Details' + '</h3>')
    response.write('<p>' + cat_list.warehouse + '</p>')
    response.write('<h3>' + 'List of products for ' + cat_list.name + ' Category' + '</h3>')
    product_list = Product.objects.filter(category__id=cat_no)
    for product in product_list:
        para = '<p>' + str(product) + ': and its price is :' + str(product.price) + '</p>'
        response.write(para)

    return render(request, 'myapp/detail.html', {'cat_list_name':cat_list.name,'cat_list_warehouse':cat_list.warehouse,'product_list':product_list})

#product method
@login_required
def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist':prodlist})

#place order for placing order
@login_required
def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                msg = 'Order placed succesfully.'
            else:
                msg = 'We dont have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html' , {'msg':msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/place_order.html', {'form':form, 'msg':msg, 'prodlist':prodlist})

#for displaying product detail
@login_required
def productdetail(request, prod_id):
    product = Product.objects.get(pk=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            data = form.data
            print('Interested:', data.get('interested'), data.get('quantity'))
            if data.get('interested') == '1':
                print('ProductInt', product.intrested)
                product.intrested = product.intrested + 1
            product.save()
        return redirect('myapp:index')
    else:
        form = InterestForm()
    return render(request, 'myapp/productdetail.html', {'form':form, 'product':product})

#for displaying user's orders on site
@login_required
def myorders(request):
    if request.session.has_key('username'):
        username=request.session['username']
        order = Order.objects.filter(client__first_name=username)
        return render(request, 'myapp/myorder.html', {'order': order})
    else:
        return HttpResponse('You are not registered client!!')
