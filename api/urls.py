from django.urls import path
from .views import YourView

urlpatterns = [
    path('', YourView.as_view(), name='your-view-name'),
    # Add more paths as needed
]
