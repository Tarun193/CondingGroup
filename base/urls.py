from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('login/',views.LoginPage, name="login"),
    path('register/',views.RegisterPage, name="register"),
    path('logout/',views.LogoutPage, name="logout"),
    path('room/<str:pk>/', views.room, name="Room"),
    path('profile/<str:pk>/', views.profilePage, name="profile-page"),
    path('create-room/', view=views.create_room, name="create-room"),
    path('create-room/<str:pk>/', view=views.update_room, name="update-room"),
    path('delete-room/<str:pk>/', view=views.delete_room, name="delete-room"),
    path('delete-message/<str:pk>/', view=views.delete_message, name="delete-message"),
    path('update-user/', view=views.edit_profile, name="update-user"),
    path('topics/', view=views.browse_topics, name="topics"),
    path('activity/', view=views.recent_activity, name="activity")
    
]