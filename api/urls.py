from user_service.views import *
from django.urls import path

urlpatterns = [
    path('register-user', register_user),
    path('login-user', login_user),
    path('list-user',list_user),
    path('update-user',update_user),
    path('delete-user', delete_user)
]
