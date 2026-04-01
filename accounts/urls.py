from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True,
        next_page='home'
    ), name='login'),

    path('logout/', LogoutView.as_view(
        next_page='home'
    ), name='logout'),

    path('register/', views.RegisterAppUserView.as_view(), name='register'),

     path('details/', views.ProfileDetailView.as_view(), name='details'),
]

