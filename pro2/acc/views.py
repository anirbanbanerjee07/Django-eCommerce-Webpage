from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from .models import Customer,Product,Tag,Order
from .forms import OrderForm,CustomerForm,ProductForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
import csv
from .forms import CreateUserForm
# Create your views here.
#######################################################################################################

# Dashboard Operations:
def registration(request):
    if request.user.is_authenticated:
        return redirect('home')
    form=CreateUserForm()
    
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,'Account was created for '+username)
            return redirect('login')
    context = {'form': form}
    return render(request,'acc/registration.html')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'username or password is incorrect...!')
    return render(request,'acc/login.html')

def logoutpage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()
    

    total_order=orders.count()
    orders_delivered=orders.filter(status='Delivered').count()
    orders_pending=orders.filter(status='Pending').count()
    out_for_delivery=orders.filter(status='Out for delivery').count()
    context={
        'total_order':total_order,
        'orders_delivered':orders_delivered,
        'orders_pending':orders_pending,
        'out_for_delivery':out_for_delivery,
        'customers':customers,
        'orders':orders,
        }
    return render(request,'acc/dashboard.html',context)

@login_required(login_url='login')
def createOrderGlobal(request):
    OrderFormSet = modelformset_factory(Order, fields=('product', 'status'), extra=3)
    customers = Customer.objects.all()

    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        customer = Customer.objects.get(id=customer_id)

        formset = OrderFormSet(request.POST, queryset=Order.objects.none())

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.customer = customer
                instance.save()
            return redirect('home')
    else:
        formset = OrderFormSet(queryset=Order.objects.none())

    context = {
        'formset': formset,
        'customers': customers
    }
    return render(request, 'acc/order_form.html', context)

@login_required(login_url='login')
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)

    OrderFormSet = modelformset_factory(Order, fields=('product', 'status'), extra=3)

    queryset = Order.objects.none()

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.customer = customer
                instance.save()
            return redirect('home')
    else:
        formset = OrderFormSet(queryset=queryset)

    context = {'formset': formset}
    return render(request, 'acc/order_form.html', context)

@login_required(login_url='login')
def select_customer_for_order(request):
    """View to select a customer before creating an order"""
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'acc/select_customer.html', context)

@login_required(login_url='login')
def createCustomer(request):
    form=CustomerForm()
    if request.method=="POST":
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'acc/create_customer.html',context)

@login_required(login_url='login')
def order_list(request):
    orders = Order.objects.all()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    return render(request, 'acc/order_list.html', {
        'orders': orders,
        'myFilter': myFilter
    })

@login_required(login_url='login')
def order_pending(request):
    orders = Order.objects.filter(status='Pending')
    context = {'orders': orders}
    return render(request, 'acc/order_pending.html', context)

@login_required(login_url='login')
def delivered_orders(request):
    orders = Order.objects.filter(status='Delivered')
    context = {'orders': orders}
    return render(request, 'acc/delivered_orders.html', context)

@login_required(login_url='login')
def out_for_delivery(request):
    orders = Order.objects.filter(status='Out for delivery')
    context = {'orders': orders}
    return render(request, 'acc/out_for_delivery.html', context)



###################################################################################################################

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'acc/product.html', context)

@login_required(login_url='login')
def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test)
    orders=customer.order_set.all()
    order_count=orders.count()

    context={
            'customer':customer,
            'orders':orders,
            'order_count':order_count
             }
    return render(request,'acc/customer.html',context)

@login_required(login_url='login')
def customers(request):
    customers=Customer.objects.all()
    return render(request,'acc/customers.html',{'customers':customers})

@login_required(login_url='login')
def image(request):
    return render(request,'acc/image.html')

@login_required(login_url='login')
def placeorder(request,pk):
    orderformset=inlineformset_factory(Customer,Order,fields=('product','status'),extra=7)
    customer=Customer.objects.get(id=pk)
    formset=orderformset(queryset=Order.objects.none(),instance=customer)
    if request.method=="POST":
        formset=orderformset(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context={'formset':formset}
    return render(request,'acc/order_form.html',context)

@login_required(login_url='login')
def updateorder(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    if request.method=="POST":
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'acc/order_form.html',context)

@login_required(login_url='login')
def deleteorder(request, pk):
    order = get_object_or_404(Order, id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('home')

    context = {'item': order}
    return render(request, 'acc/delete.html', context)

@login_required(login_url='login')
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'acc/customer_form.html', context)

@login_required(login_url='login')
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)

    if request.method == 'POST':
        customer.delete()
        return redirect('home')

    context = {'item': customer}
    return render(request, 'acc/delete_customer.html', context)

@login_required(login_url='login')
def Customer_list(request):
    customer=Customer.objects.all()
    context={'customer':customer}
    return render(request,'acc/customer_list.html',context)

@login_required(login_url='login')
def addProduct(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product')  

    context = {'form': form}
    return render(request, 'acc/add_product.html', context)

@login_required(login_url='login')
def update_product(request,pk):
    product=Product.objects.get(id=pk)
    form=ProductForm(instance=product)
    
    old_image = product.pic
    
    if request.method=="POST":
        pic_clear = request.POST.get('pic-clear')
        
        form=ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if 'pic' in request.FILES:
                if old_image:
                    old_image.delete(save=False)
            elif pic_clear == 'on' and old_image:
                product.pic = None
                old_image.delete(save=False)
            
            form.save()
            return redirect('product')
    context={'form':form, 'product': product}
    return render(request,'acc/add_product.html',context)

@login_required(login_url='login')
def deleteProduct(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        if product.pic:
            product.pic.delete(save=False)
        product.delete()
        return redirect('product')

    context = {'item': product}
    return render(request, 'acc/delete_product.html', context)
#####################################################################################################


#tag list
    
@login_required(login_url='login')
def tag_list(request):
    tag=Tag.objects.all()
    context={'tag':tag}
    return render(request,'acc/tag.html',context)

@login_required(login_url='login')
def importtag(request):
    if request.method=='POST':
        csv_file=request.FILES.get("file")
        decoded_file=csv_file.read().decode("utf-8").splitlines()
        reader=csv.DictReader(decoded_file)

        for row in reader:
            Tag.objects.get_or_create(name=row["name"])
        return redirect('tag')
    return render(request,'acc/tag_m.html')
