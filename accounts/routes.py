from django.shortcuts import render, HttpResponse, Http404, redirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
from .models import product, ssl
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

# Create your views here.

# Home Page 
def index(request):
    return render(request, '../templates/ssllist.html')
    
def postdata(message):
    serial = message['serial']
    status = message['stat']
    battery_status = message['batstat']
    battery_voltage = message['volt']
    power_panel = message['powpanel']
    panel_voltage = message['panelvolt']
    Energy_curr = message['engcurr']
    Total_energy = message['totaleng']
    print(serial)
    
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
# @permission_required('accounts.add_user')
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
def sslData(request):
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
            elif user.has_perm('accounts.view_product'):
                return redirect('Dashboard')
    return render(request,'../templates/login_view.html')

@login_required(login_url='/login')
def logout_view(request):
    return logout(request)

@login_required(login_url='/login')
def ControlSSL(request):
    return

@login_required(login_url='/login')
@permission_required('accounts.view_user')
def main_menu(request):
    if request.method=='GET':
        name = request.user.username
        print('Hi '+name)
        products = product.objects.filter(belongs_to__username=name)
        products = list(products)
        print(products[0].serial_no)
        livessl = product.objects.filter(belongs_to__username=name,status='on').values('serial_no').distinct().count()
        total = product.objects.filter(belongs_to__username=name).values('serial_no').distinct().count()
        context = {
            'products': products,
            'livessl' : livessl,
            'total'   : total,
        }
        return render(request, '../templates/table.html',context)
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
        return render(request, '../templates/table.html',context)
    return redirect('/login')

@login_required(login_url='/login')
def dashboard(request):
    if request.method == 'POST':
        print(request.method)
        if request.user.authenticated: 
            choice = request.GET['choice']
            return redirect('Dashboard')
    print(request.method)
    return render(request,'../templates/dashboard.html')

@login_required(login_url='/login')
def admin_home(request):
    if request.method == 'GET':
        if request.user.authenticated and request.user.objects.filter(group__name = 'Admin'): 
            agency_list = User.objects.filter(group__name = 'Agency')
            agency_list = list(agency_list)
            context={
                'agency_list':agency_list,
            }
            return render('../templates/admin_home.html', context)
    return Http404

@login_required(login_url='/login')
def user_list(request):
    if request.user.authenticated:
        if request.method=='GET':
            name = request.user.username
            livessl = product.objects.filter(belongs_to__username=name,status='on').values('serial_no').distinct().count()
            total = product.objects.filter(belongs_to__username=name).values('serial_no').distinct().count()
            users = User.objects.filter(group__name = name)
            context = {
                'products': products,
                'livessl' : livessl,
                'total'   : total,
                'userlist':users,
            }
            return render(request, '../templates/user_list.html',context)
        elif request.method == 'POST': 
            name = request.POST['username']
            location = request.POST['location']
            if name is None:
                userlist = agency.objects.filter(group__name = request.user.username,username=name, last_name = location)
            elif location is None:
                userlist = agency.objects.filter(group__name = request.user.username,username=name, last_name = location)
            else:
                userlist = agency.objects.filter(group__name = name, last_name = location)
            livessl = product.objects.filter(belongs_to__username=name,status='on').values('serial_no').distinct().count()
            total = product.objects.filter(belongs_to__username=name).values('serial_no').distinct().count()
            context = {
                'products': products,
                'livessl' : livessl,
                'total'   : total,
                'userlist':userlist,
            }
            return render(request,'../templates/user_list.html',context)
    return Http404

def ssl_list(request):
    if request.user.authenticated:
        if request.method == 'GET':
            user = request.user.username
            ssl = ssl.object.filter(belongs_to__username = user)
            context = {
                'ssl_list':ssl,
            }
            return render(request,'../templates/ssl_list.html')
        if request.method == 'POST':
            user = request.POST['user']
            ssl = ssl.object.filter(belongs_to__username = user)
            context = {
                'ssl_list':ssl,
            }
            return render(request,'../templates/ssl_list.html')
    return Http404

def ssl_data(request):
    if request.user.authenticated:
        if request.method == 'GET':
            serial = request.GET['serial']
            ssl = product.object.filter(serial_no = serial)
            context = {
                'ssl_data':ssl,
            }
            return render(request,'../templates/ssl_data.html')
    return Http404