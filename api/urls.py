from django.urls import path
from .views import YourView, LoginView, LogoutView

urlpatterns = [
    path('', YourView.as_view(), name='your-view-name'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Add more paths as needed
]
