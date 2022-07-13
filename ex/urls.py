"""test_pa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('Login/', views.Login.as_view(), name='Login'),
    path('logout/',views.Logout.as_view(), name='logout'),
    path('superuser/?P<int:pk>/',views.SuperUser, name='super'),
    path('admin/?P<int:pk>/',views.Admin, name='admin'),
    path('staff/',views.Staff, name='staff'),
    path('add_admin/',views.add_admin, name='staff'),
    path('register/', views.Register.as_view(), name='register'),
    path('log/', views.is_login, name='register'),
    path('user_profile/?P<int:pk>/', views.user_profile, name='profile'),
    path('edit/?P<int:pk>/',views.Details.as_view(), name='edit'),
    path('populate/', views.Populate.as_view(), name='populate'),
    path('populatecom/', views.PopulateCom.as_view(), name='populatecom'),
    path('comment/?P<int:pk>/',views.ComCom.as_view(), name='comment'),
    path('forums/', views.PostDisplay.as_view(), name='forum'),
    path('details/?P<int:pk>/',views.Publish.as_view(), name='details'),
    path('publishpost/', views.RegisterPost.as_view(), name='post'),
]
