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
    path('calories_graph/', views.calories_graph, name="calories_graph"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    # custom bmr view
    path('custom_bmr/', views.custom_bmr_view, name="custom_bmr"),
    # BMR handler
    path('bmr_handler/', views.bmr_handler, name="bmr_handler"),
    # delete_food_item
    path('delete_food_item/<delete_id>', views.delete_food_item, name="delete_food_item"),
]
