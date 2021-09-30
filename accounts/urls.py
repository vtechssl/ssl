from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='Login'),
    path('home',views.board,name='Board'),
    path('table',views.ViewProduct,name='Table'),
    path('dashboard',views.dashboard,name='Dashboard'),
    path('post-data',views.postdata,name='post_data'),
    path('login',views.login_view,name='Login'),
    path('logout',views.logout,name='Logout'),
    path('createuser',views.CreateUser,name='CreateUser'),
    path('createproduct',views.CreateProduct,name='CreateProduct'),
    path('viewagencies',views.ViewAgencies,name='ViewAgencies'),
    path('viewproductforagency',views.ViewProductsforAgency,name='ViewProductforAgencies'),
    path('deleteuser',views.DeleteUser,name='DeleteUser'),
    path('addssl',views.AssignUsertoProduct,name='AssignUsertoProduct'),
    path('controlssl',views.ControlSSL,name='ControlSSL'),
    path('view',views.View,name='View'),
]