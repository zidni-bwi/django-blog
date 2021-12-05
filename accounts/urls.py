from django.urls import path
from accounts import views as account_views
from django.contrib.auth import views as auth_views

from .views import CustomLoginView
from .forms import LoginForm

urlpatterns = [
    path('accounts/', account_views.Index, name='index_accounts'),
    path('edit_accounts/', account_views.Edit, name='edit_accounts'),
    path('edit_password/', account_views.PasswordChangeView.as_view(template_name='edit_password.html'), name='edit_password'),

    path('register/', account_views.Register, name='register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='auth/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


]
