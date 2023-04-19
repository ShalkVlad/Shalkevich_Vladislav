from django.urls import path

from accounts.views import signup, user_login
from hello import views

app_name = 'accounts'
urlpatterns = [
    path('login/', user_login, name='login'),
    path('', views.hello, name='hello'),
    path('register/', signup, name='register'),
]
