from django.urls import path
from weatherapp import views

urlpatterns = [
    path('',views.homeview,name='home'),
    path('signin/',views.signinview,name='signin'),
    path('signup/',views.signupview,name='signup'),
    path('signout/',views.signoutview,name='signout'),
    path('weather/',views.weather,name='weather')
]

