from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='sso_login'),
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('authenticate/', views.authenticate, name='authneticate'),


]
