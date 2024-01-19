from rest_framework.views import APIView
from rest_framework.response import Response


class YourView(APIView):
    def get(self, request):
        return Response({"message": "Hello, DRF!"})
