from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name='career'),
    path('login',views.login_views,name='login'),
    path('AdminPanel',views.admin_views,name='AdminPanel'),
    path('User',views.User_views,name='User'),
    path('approved/<int:pk>',views.feedback_approval,name='approved'),
    path('delete/<int:pk>',views.feedback_delete,name='delete'),
    path('logout',views.logout_views,name='logout'),

]
