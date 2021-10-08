from django.shortcuts import render, HttpResponse, Http404, redirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import product
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

# Create your views here.

def is_superadmin(user):
    return user.groups.filter(name='SuperAdmin').exists()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_agency(user):
    return user.groups.filter(name='Agency').exists()

def is_user(user):
    return user.groups.filter(name='User').exists()

# Home Page 
def index(request):
    return render(request, '../templates/ssllist.html')

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
    return HttpResponse("Data updated")

@login_required(login_url='/login')
@user_passes_test(is_admin)
def admin_home(request):
    if request.method == 'GET':
        if request.user.is_authenticated: 
            agency_list = User.objects.filter(groups__name='Admin')
            agency_list = list(agency_list)
            context={
                'agency_list':agency_list,
            }
            return render(request,'../templates/admin_home.html', context)
    return Http404

@login_required(login_url='/login')
@user_passes_test(is_agency)
def user_list(request):
    if request.user.is_authenticated:
        if request.method=='GET':
            name = request.user.username
            livessl = product.objects.filter(belongs_to__username=name,status='on').values('serial_no').distinct().count()
            total = product.objects.filter(belongs_to__username=name).values('serial_no').distinct().count()
            users = User.objects.filter(groups__name = name)
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
                userlist = agency.objects.filter(groups__name = request.user.username,username=name, last_name = location)
            elif location is None:
                userlist = agency.objects.filter(groups__name = request.user.username,username=name, last_name = location)
            else:
                userlist = agency.objects.filter(groups__name = name, last_name = location)
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

@login_required(login_url='/login')
@user_passes_test(is_user)
def ssl_list(request):
    if request.user.is_authenticated:
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

@login_required(login_url='/login')
@user_passes_test(is_user)
def ssl_data(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            serial = request.GET['serial']
            ssl = product.object.filter(serial_no = serial)
            context = {
                'ssl_data':ssl,
            }
            return render(request,'../templates/ssl_data.html')
    return Http404

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(request.POST)
        user = authenticate(request,username=username, password=password)
        if user is None:
            return redirect('login')
        else:
            login(request, user)
            if user.groups.filter(name='Admin').exists():
                return redirect('AdminHome')
            elif user.groups.filter(name='Agency').exists():
                return redirect('AgencyHome')
            elif user.groups.filter(name='User').exists():
                return redirect('sslList')
    return render(request,'../templates/login_view.html')

@login_required(login_url='login')
def logout_view(request):
    return logout(request)
