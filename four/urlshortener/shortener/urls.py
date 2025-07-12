from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # URL management
    path('dashboard/', views.url_list, name='dashboard'),
    path('add/', views.add_url, name='add_url'),
    path('edit/<int:id>/', views.edit_url, name='edit_url'),
    path('delete/<int:id>/', views.delete_url, name='delete_url'),

    # Search results (optional if you're using separate page)
    path('search/results/', views.search_results, name='search_results'),

    # Redirect by short URL
    path('<str:code>/', views.redirect_url, name='redirect_short_url'),
    path('shorten/', views.shorten_url_view, name='shorten_url'),

]
