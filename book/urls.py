from django.urls import path ,reverse_lazy, include
from book import views
from django.contrib.auth import views as as_view
from django.contrib.auth import views as auth_views #import this
from django.conf.urls.static import static
from django.conf import settings
from .views import PasswordChangeView
urlpatterns = [
    path('' , views.home, name="home"),
    path('book/' , views.books, name= "all_books"),
    path('book/new/', views.add_book , name= "add_book"),
    path('book/<pk>/', views.view_book ,name = "view_book"),
    path('book/<pk>/edit' , views.edit_book  ,name= "edit_book"), 
    path('book/<pk>/delete' , views.delete_book , name = "delete_book"),
    path('book/<pk>/addtofave' , views.favorite_book , name="favorite_book"),
    path('book/<pk>/wantToRead' , views.wantToRead , name="wantToRead"),
    path('signin/' , as_view.LoginView.as_view(template_name = "user/signin.html") , name= "signin"),
    path('register/' , views.register , name= "register"),
    path('logout/' , as_view.LogoutView.as_view() , name= "logout") , 
    path('home/', views.home, name='home'),
    path('profile/<pk>' , views.profile , name="profile" ),
    path('profile/edit/<pk>' , views.Profile_edit , name="profile_edit" ),
    path('profile/setting/<pk>' , views.Setting , name="setting" ),
    path('book/<pk>/comment/add', views.add_comment ,name = "add_comment"),
    path('book/<pk>/comment/edit/<pkb>' , views.edit_comment  ,name= "edit_comment"),
    path('book/<pk>/comment/delete' , views.delete_comment , name = "delete_comment"),
    path('search/' , views.Search , name = "search"),
    path('search_by_type/<mtype>' , views.search_by_type , name = "search_by_type"),
    path('book/<pk>/rating' , views.add_rate , name = "add_rating"),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='reset-password'),
    path('reset-password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_change', PasswordChangeView.as_view(template_name='auth/password_change.html'), name='password_change'),
    path('password_change_done', views.PasswordChangeDone, name='password_change_success'),
    path('show_books', views.show_books, name='show_books'),

] + static(settings.MEDIA_URL , document_root= settings.MEDIA_ROOT)








