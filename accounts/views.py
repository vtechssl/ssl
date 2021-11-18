from django.shortcuts import render, HttpResponse, Http404, redirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import product, ssl
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import xlwt

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

    return render(request, '../templates/superadmin.html')

@csrf_exempt
def postdata(request):
    # b1c9307d-2786-469d-b158-b223f23bf1a9
    print()
    print(request.headers)
    print(request.body)
    print()
    print()
    print()
    print()
    serial = request.POST['serial']
    status = request.POST['stat']
    battery_status = request.POST['batstat']
    battery_voltage = request.POST['volt']
    power_panel = request.POST['powpanel']
    panel_voltage = request.POST['panelvolt']
    Energy_curr = request.POST['engcurr']
    Total_energy = request.POST['totaleng']
    print(serial)
    
    pr = ssl.objects.filter(serial_no=serial)

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
    return HttpResponse('Data updated')

@login_required(login_url='/login')
@user_passes_test(is_superadmin)
def superadmin_home(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            agency_list = User.objects.filter(groups__name='Agency')
            agency_list = list(agency_list)
            context={
                'agency_list':agency_list,
            }
            return render(request, '../templates/superadmin.html',context)

@login_required(login_url='/login')
@user_passes_test(is_superadmin)
def superadmin_users(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user_list = User.objects.filter(groups__name='User')
            user_list = list(user_list)
            agency_list = User.objects.filter(groups__name='Agency')
            agency_list = list(agency_list)
            context={
                'user_list':user_list,
                'agency_list':agency_list,
            }
            return render(request, '../templates/superadmin_user.html',context)

@login_required(login_url='/login')
@user_passes_test(is_admin)
def admin_home(request):
    if request.user.is_authenticated:
        if request.method == 'GET': 
            agency_list = User.objects.filter(groups__name='Agency')
            agency_list = list(agency_list)
            context={
                'agency_list':agency_list,
            }
            return render(request,'../templates/admin_home.html', context)
    messages.warning(request, 'Invalid Request')
    return Http404

@login_required(login_url='/login')
@user_passes_test(is_agency)
def agency_home(request):
    if request.user.is_authenticated:
        if request.method=='GET':
            name=''
            try:
                name = request.GET['username']  
            except:
                name = request.user.username
            print(name)
            livessl = product.objects.filter(belongs_to__username=name,status='on').values('serial_no').distinct().count()
            total = product.objects.filter(belongs_to__username=name).values('serial_no').distinct().count()
            users = User.objects.filter(groups__name = name)
            print(users)
            context = {
                'livessl' : livessl,
                'total'   : total,
                'userlist':users,
            }
            return render(request, '../templates/user_list.html',context)
        elif request.method == 'POST': 
            name = request.POST['username']
            location = request.POST['location']
            userlist = User.objects.filter(username=name, last_name = location)
            livessl = product.objects.filter(belongs_to__username=name,status='on').values('serial_no').distinct().count()
            total = product.objects.filter(belongs_to__username=name).values('serial_no').distinct().count()
            context = {
                'livessl' : livessl,
                'total'   : total,
                'userlist':userlist,
            }
            return render(request,'../templates/user_list.html',context)
    messages.warning(request, 'Invalid Request')
    return Http404

@login_required(login_url='/login')
# @user_passes_test(is_user)
def ssl_list(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user.username
            ssls = ssl.objects.filter(belongs_to__username = user)
            ssls = list(ssls)
            context = {
                'ssl_list':ssls,
            }
            return render(request,'../templates/ssl_list.html',context)
        if request.method == 'POST':
            user = request.POST['username']
            ssls = ssl.objects.filter(belongs_to__username = user)
            ssls = list(ssls)
            print(ssls)
            context = {
                'ssl_list':ssls,
            }
            return render(request,'../templates/ssl_list.html',context)
    return Http404

@login_required(login_url='/login')
# @user_passes_test(is_user)
def ssl_data(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            serial = request.POST['serial']
            ssls = product.objects.filter(serial_no = serial)
            ssls = list(ssls)
            ssls = ssls.reverse()
            print(ssls)
            context = {
                'ssl_data':ssls,
            }
            return render(request,'../templates/ssl_data.html',context)
    messages.warning(request, 'Invalid Request')
    return Http404

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(request.POST)
        user = authenticate(request,username=username, password=password)
        if user is None:
            messages.warning(request, 'Invalid Credentials')
            return redirect('Login')
        else:
            login(request, user)
            print(Group.objects.all())
            messages.success(request, 'Login Successful')
            if user.groups.filter(name='SuperAdmin').exists():
                return redirect('SuperAdmin')
            elif user.groups.filter(name='Admin').exists():
                return redirect('AdminHome')
            elif user.groups.filter(name='Agency').exists():
                return redirect('AgencyHome')
            elif user.groups.filter(name='User').exists():
                return redirect('sslList')
    return render(request,'../templates/login_view.html')

@login_required(login_url='login')
def logout_view(request):
    messages.info(request, 'Logout Successful')
    logout(request)
    return redirect('Login')

@login_required(login_url='login')
def temp(request):
    return redirect('sslList')

@login_required(login_url='/login')
@user_passes_test(is_superadmin)
def modify_data(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            serial = request.POST['serial']
            status = request.POST['stat']
            location = request.POST['location']
            battery_status = request.POST['batstat']
            battery_voltage = request.POST['volt']
            power_panel = request.POST['powpanel']
            panel_voltage = request.POST['panelvolt']
            Energy_curr = request.POST['engcurr']
            Total_energy = request.POST['totaleng']
            timestamp = request.POST['timestamp']

            pr = product.objects.get(updated_at=timestamp)

            pr.updated_at=timestamp
            pr.serial_no=serial
            pr.location=location
            pr.status=status
            pr.battery_status=battery_status
            pr.battery_voltage=battery_voltage
            pr.power_panel=power_panel
            pr.panel_voltage=panel_voltage
            pr.energy_curr=Energy_curr
            pr.total_energy=Total_energy
            pr.save()
            messages.success(request, 'Data Updated')
            return redirect('sslData')

@login_required(login_url='/login')
@user_passes_test(is_superadmin)
def addAgency(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['name']
            user = User.objects.create_user(username=username, password=password, first_name=first_name)
            user.save()
            group = Group.objects.get(name='Agency') 
            group.user_set.add(user)
            new_group, created = Group.objects.get_or_create(name=username)
            return redirect('SuperAdmin')
        elif request.method == 'GET':
            return render(request, '../templates/add_agency.html')

@login_required(login_url='/login')
@user_passes_test(is_superadmin)
def addAdmin(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['name']
            user = User.objects.create_user(username=username, password=password, first_name=first_name)
            user.save()
            group = Group.objects.get(name='Admin')
            group.user_set.add(user)
            # group = Group.objects.get_or_create(name=username)
            # group.save()
            new_group, created = Group.objects.get_or_create(name=username)
            return redirect('SuperAdmin')

@login_required(login_url='/login')
@user_passes_test(is_superadmin)
def addUser(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['name']
            location = request.POST['location']
            agency = request.POST['agency']
            print(agency)
            user = User.objects.create_user(username=username, password=str(password), first_name=first_name, last_name=location)
            user.save()
            group = Group.objects.get(name='User') 
            group.user_set.add(user)
            group = Group.objects.get(name=agency) 
            group.user_set.add(user)
            return redirect('SuperAdminU')
        elif request.method == 'GET':
            return render(request, '../templates/add_user.html')

@login_required(login_url='/login')
@user_passes_test(is_superadmin)
def registerProduct(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            serial = request.POST['serial']
            users = request.user
            new_ssl = ssl(serial_no=serial)
            new_ssl.save()
            new_ssl.belongs_to.add(users)
            return redirect('RegisterSSL')
        elif request.method == 'GET':
            ssls = ssl.objects.filter(belongs_to = request.user)
            user_list = User.objects.filter(groups__name='User')
            user_list = list(user_list)
            agency_list = User.objects.filter(groups__name='Agency')
            agency_list = list(agency_list)
            context={
                'user_list':user_list,
                'agency_list':agency_list,
                'products':ssls,
            }
            return render(request, '../templates/registerssl.html',context)

@login_required(login_url='/login')
@user_passes_test(is_superadmin)
def Assign(request):
    if request.method=='POST':
        serial = request.POST['serial']
        agency=request.POST['agency']
        user=request.POST['user']
        print(user)
        new_ssl = ssl.objects.get(serial_no=serial)
        user = User.objects.get(username=user)
        agency = User.objects.get(username=agency)
        new_ssl.belongs_to.add(agency)
        new_ssl.belongs_to.add(user)
        new_ssl.belongs_to.remove(request.user)
        return redirect('RegisterSSL')

@login_required(login_url='login')
def delete(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            usernames = request.POST['username']
            user = User.objects.get(username=usernames)
            user.delete()
            return redirect('SuperAdmin')
        if request.method == 'GET':
            serial = request.POST['serial']
            ssls = ssl.objects.get(serial_no=serial)
            ssls.delete()
            ssls = product.objects.filter(serial_no=serial)
            ssls.delete()
            return redirect('sslList')
        if request.method == 'PUT':
            time = request.POST['time']
            ssls = product.objects.get(updated_at=time)
            ssls.delete()
            return redirect('sslData')


@login_required(login_url='/login')
def download(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            response = HttpResponse(content_type='application/ms-excel')
            name = request.POST['file_name']
            response['Content-Disposition'] = f'attachment; filename="{name}.xls"'


            #creating workbook
            wb = xlwt.Workbook(encoding='utf-8')

            #adding sheet
            ws = wb.add_sheet("sheet1")

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            # headers are bold
            font_style.font.bold = True

            serial = request.POST['serial']
            ssl = product.objects.filter(serial_no = serial)

            ssl = list(ssl)
            # ssl = ssl.reverse()

            #column header names, you can use your own headers here
            columns = ['Created at', 'Updated at', 'Serial No', 'Location', 'Status', 'Battery Status', 'Battery Voltage', 'Panel Power', 'Panel Voltage', 'Current Energy', 'Total Energy', 'Belongs to']

            #write column headers in sheet
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            #get your data, from database or from a text file...
            for row in ssl:
                row_num = row_num + 1
                ws.write(row_num, 0, str(row.created_at), font_style)
                ws.write(row_num, 1, str(row.updated_at), font_style)
                ws.write(row_num, 2, row.serial_no, font_style)
                ws.write(row_num, 3, row.location, font_style)
                ws.write(row_num, 4, row.status, font_style)
                ws.write(row_num, 5, row.battery_status, font_style)
                ws.write(row_num, 6, row.battery_voltage, font_style)
                ws.write(row_num, 7, row.power_panel, font_style)
                ws.write(row_num, 8, row.panel_voltage, font_style)
                ws.write(row_num, 9, row.energy_curr, font_style)
                ws.write(row_num, 10, row.total_energy, font_style)
                cnt = 11
                temp = list(row.belongs_to.all())
                for p in temp:
                    ws.write(row_num, cnt, p.username, font_style)
                    cnt = cnt+1

            wb.save(response)
            return response