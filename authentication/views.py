from authentication.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from authentication.serializers import UserSerializer
from rest_framework import status, response


class UserSignupView(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
