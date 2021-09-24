from django.shortcuts import render, HttpResponse, Http404, redirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
from .models import product
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

# Create your views here.

# Home Page 
def index(request):
    return render(request, '../templates/home.html')
@csrf_exempt
def postdata(request):
    print()
    print(request.headers)
    print(request.body)
    print()
    print()
    print()
    print()
    serial = request.POST["serial"]
    status = request.POST["stat"]
    battery_status = request.POST["batstat"]
    battery_voltage = request.POST["volt"]
    power_panel = request.POST["powpanel"]
    panel_voltage = request.POST["panelvolt"]
    Energy_curr = request.POST["engcurr"]
    Total_energy = request.POST["totaleng"]
    
    pr = product.objects.filter(serial_no=serial)

    if pr is None:
        return HttpResponse('serial no not found')
    #   
    l = list(pr)
    print(pr)
    new = product(serial_no=serial,location='Nagpur',attribute='0',status=status,battery_status=battery_status,battery_voltage=battery_voltage,power_panel=power_panel,panel_voltage=panel_voltage,energy_curr=Energy_curr,total_energy=Total_energy)
    users = l[0].belongs_to.all()
    print(users)
    new.save()
    for i in users:
        new.belongs_to.add(i)
    new.save()
    return HttpResponse("Data updated")

@login_required(login_url='/login')
@permission_required('accounts.add_user')
def CreateUser(request):
    if request.method == 'POST' and request.user.is_superuser:
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['type']
        
        if not username.endswith('@vtech.co.in'):
            return redirect('createuser')
        
        if user_type != 'agency' and user_type != 'user':
            return redirect('createuser')
        
        user = User.objects.create_user(name=name,username=username,password=password)
        user.save()

        if user_type == 'agency':
            group = Group.objects.get(name='Agencies')
            group.user_set.add(user)
        else:
            group = Group.objects.get(name='User')
            group.user_set.add(user)
        return 
    return Http404

@login_required(login_url='/login')
@permission_required('accounts.add_user')
def CreateProduct(request):
    if request.method == 'POST' and request.user.is_superuser:
        serialno = request.POST['serial']
        location = request.POST['location']
        products = product(serial_no=serialno,location=location,attribute='0')
        products.belongs_to.add(request.user)
        products.save()
    return Http404

@login_required(login_url='/login')
@permission_required('accounts.add_user')
def AssignUsertoProduct(request):
    if request.method == 'POST' and request.user.is_superuser:
        serialno = request.POST['serial']
        username = request.POST['username']
        user = User.objects.get(username=username,is_active=True)
        products = product.objects.get(serial_no=serialno)
        product.belongs_to.add(user)
        product.save()
    return Http404

@login_required(login_url='/login')
@permission_required('accounts.delete_user')
def DeleteUser(request):
    if request.method == 'POST' and request.user.is_superuser:
        username = request.POST['username']
        user = User.objects.get(username=username,is_active=True)
        user.is_active = False
        user.save()
    return Http404

@login_required(login_url='/login')
@permission_required('accounts.add_user')
def ViewAgencies(request):
    if request.user.is_superuser:
        agencies = User.objects.get(groups='Agencies')
        return
    pass

@login_required(login_url='/login')
@permission_required('accounts.add_user')
def View(request):
    if request.method == 'GET' and request.user.is_superuser:
        name = request.POST['name']
        agency = User.objects.get(first_name=name)
        return
    pass

@login_required(login_url='/login')
@permission_required('accounts.add_user')
def ViewProductsforAgency(request):
    if request.method == 'POST' and request.user.is_superuser:
        agency = request.POST['agency']
        agency_products = product.objects.get(belongs_to=agency)
        return
    pass

@login_required(login_url='/login')
@permission_required('accounts.view_group')
def ViewUsers(request):
    if request.method == 'POST' and request.user.is_superuser:
        users = User.objects.get(groups="User")
        return
    pass

@login_required(login_url='/login')
def ViewProduct(request):
    if request.method == 'POST':
        serial = request.POST['serial']
        print(request.POST)
        e_date = request.POST.get('date')
        if e_date is not None:
            products = product.objects.filter(serial_no=serial,updated_at__icontains=e_date)
        else:
            products = product.objects.filter(serial_no=serial)
        if products is None:
            print('None')
            return Http404
        products = list(products)
        products.reverse()
        users = [i.belongs_to.all() for i in products ]
        print(products[0].updated_at)
        context = {
            'products': products,
            'user': users
        }
        return render(request, '../templates/table.html',context)
    return render(request, '../templates/table.html')

@login_required(login_url='/login')
@permission_required('accounts.add_user')
def ChangePassword(request):
    if request.method == 'POST' and request.user.is_superuser:
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username)
        user.set_password(password)
    return

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(request.POST)
        user = authenticate(request,username=username, password=password)
        if user is None:
            return redirect('/login')
        else:
            login(request, user)
            if user.has_perm('auth.view_user'):
                return redirect('/home')
            elif user.has_perm('auth.view_product'):
                return redirect('Dashboard')
    return render(request,'../templates/login.html')

@login_required(login_url='/login')
def logout_view(request):
    logout(request)

@login_required(login_url='/login')
def ControlSSL(request):
    return

@login_required(login_url='/login')
# @permission_required('accounts.view_user')
def dashboard(request):
    if request.method=='GET':
        name = request.user.username
        print('Hi '+name)
        products = product.objects.filter(belongs_to__username=name).values('serial_no').distinct()
        products = list(products)
        livessl = product.objects.filter(belongs_to__username=name,status='on').values('serial_no').distinct().count()
        total = product.objects.filter(belongs_to__username=name).values('serial_no').distinct().count()
        context = {
            'products': products,
            'livessl' : livessl,
            'total'   : total,
        }
        return render(request, '../templates/home.html',context)
    elif request.user.is_authenticated and request.method=='POST':
        name = request.user.username
        serial = request.POST['serial']
        products = product.objects.filter(belongs_to__username=name,serial_no=serial).values('serial_no').distinct()
        products = list(products)
        livessl = product.objects.filter(status='on').values('serial_no').distinct().count()
        total = product.objects.filter(belongs_to__username=name).values('serial_no').distinct().count()
        context = {
            'products': products,
            'livessl' : livessl,
            'total'   : total,
        }
        return render(request, '../templates/home.html',context)
    return redirect('/login')

@login_required(login_url='/login')
# @permission_required('accounts.view_users')
def board(request):
    if request.method == 'POST':
        print(request.method)
        if request.user.authenticated: 
            choice = request.GET['choice']
            return redirect('Dashboard')
    print(request.method)
    return render(request,'../templates/dashboard.html')