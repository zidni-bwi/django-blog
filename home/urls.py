from django.urls import path
from home import views

urlpatterns = [

    path('', views.Home, name='home'),

    path('detail_posts/<id_post>', views.Detail_Posts, name='detail_posts'),

]
