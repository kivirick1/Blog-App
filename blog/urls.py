from django.urls import path
from .views import * 

urlpatterns = [
    # Auth
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    
    # Home
    path('', home, name='home'),
    
    # Blog
    path('blog/create/', blog_create, name='blog_create'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('blog/<slug:slug>/update/', blog_update, name='blog_update'),
    path('blog/<slug:slug>/delete/', blog_delete, name='blog_delete'),
    
    # Comment
    path('blog/<slug:slug>/comment/', comment_create, name='comment_create'),
    path('comment/<int:pk>/update/', comment_update, name='comment_update'),
    path('comment/<int:pk>/delete/', comment_delete, name='comment_delete'),
    
    # Like
    path('blog/<slug:slug>/like/', like_toggle, name='like_toggle'),
    
    # Category
    path('categories/', category_list, name='category_list'),
    path('category/create/', category_create, name='category_create'),
    path('category/<int:pk>/update/', category_update, name='category_update'),
    path('category/<int:pk>/delete/', category_delete, name='category_delete'),
]