from django.urls import path
from .views import YourView, LoginView

urlpatterns = [
    path('', YourView.as_view(), name='your-view-name'),
    # path('login/', LoginView.as_view(), name='login'),
    # Add more paths as needed
]
