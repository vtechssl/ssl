from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view,name='Login'),
    path('AdminHome',views.admin_home,name='AdminHome'),
    path('AgencyHome',views.user_list,name='AgencyHome'),
    path('UserList',views.user_list,name='UserList'),
    path('sslList',views.ssl_list,name='sslList'),
    path('sslData',views.ssl_data,name='SSLData'),
    path('post-data',views.postdata,name='post_data'),
    path('login',views.login_view,name='Login'),
    path('logout',views.logout_view,name='Logout'),
]