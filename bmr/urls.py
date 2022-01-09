from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.sign_in, name="sign_in"),
    path('logout/', views.user_logout, name="logout"),
    path('addfooditem/', views.add_food_item, name="addfooditem"),
    path('delete_bmr/<delete_id>', views.delete_bmr),
    path('calories_detail/', views.calories_detail, name="calories_detail"),
]
