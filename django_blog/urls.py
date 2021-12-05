from django.urls import path, include
from dashboard import views as dashboard
from members import views as members

urlpatterns = [
    path('', include('home.urls')),

    path('', include('posts.urls')),

    path('', include('accounts.urls')),

    path('dashboard/', dashboard.Index, name='dashboard'),

    path('members/', members.Index, name='members'),
]
