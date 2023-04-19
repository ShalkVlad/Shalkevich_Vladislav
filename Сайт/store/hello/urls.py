from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts import views
from .views import hello, feedback, parsing_order

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', hello, name='hello'),
    path('login/', views.user_login, name='login'),
    path('login/register/', views.signup, name='register'),
    path('parsing-order/', parsing_order, name='parsing_order'),
    path('feedback/', feedback, name='feedback'),
]
