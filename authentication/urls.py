from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('activate/<str:token>/', views.activate_account, name = 'activate_account'),
    path('recover/', views.recover_password_email, name = 'recover_password_email'),
    path('recover/<str:token>', views.recover_password, name = 'recover_password'),
    path('norecover/<str:token>', views.norecover_password, name = 'norecover_password')
]