from rest_framework.routers import DefaultRouter
from django.urls import path, include
from accounts import views


urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('verify/<token>/<uid64>/', views.is_active, name='is_active'),
    # path('profile/list/', views.ProfileView.as_view(), name='profile'),
    path('profile/list/view/', views.ProfileListView.as_view(), name='profile_list_view'),
    path('myprofile/', views.EditProfileView.as_view(), name='profile'),
]