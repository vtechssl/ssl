from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view,name='Login'),
    path('SuperAdmin',views.superadmin_home,name='SuperAdmin'),
    path('SuperAdminU',views.superadmin_users,name='SuperAdminU'),
    path('AdminHome',views.admin_home,name='AdminHome'),
    path('AddAgency',views.addAgency,name='AddAgency'),
    path('AddUser',views.addUser,name='AddUser'),
    path('AgencyHome',views.agency_home,name='AgencyHome'),
    path('UserList',views.agency_home,name='UserList'),
    path('sslList',views.ssl_list,name='sslList'),
    path('sslData',views.ssl_data,name='SSLData'),
    path('post-data',views.postdata,name='post_data'),
    path('login',views.login_view,name='Login'),
    path('logout',views.logout_view,name='Logout'),
]