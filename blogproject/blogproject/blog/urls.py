from django.urls import path
from . import views

urlpatterns = [

path('', views.post_list, name='post_list'),

path('register/', views.register, name='register'),

path('login/', views.login_view, name='login'),

path('logout/', views.logout_view, name='logout'),

path('create/', views.create_post, name='create_post'),

path('update/<int:id>/', views.update_post, name='update_post'),

path('delete/<int:id>/', views.delete_post, name='delete_post'),
path('view_all/', views.view_all_posts, name='view_all_posts'),

]