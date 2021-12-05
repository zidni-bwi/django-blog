from django.urls import path
from posts import views

urlpatterns = [
    path('posts/', views.index, name='index_posts'),
    path('add_posts/', views.add, name='add_posts'),
    path('edit_posts/<posts_id>', views.edit, name='edit_posts'),
]
