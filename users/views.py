from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer, ReadUserSerializer, WriteUserSerializer


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serialized_user = ReadUserSerializer(request.user)
        return Response(data=serialized_user.data)

    def put(self, request):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
        print(serializer.is_valid())
        if serializer.is_valid():
            user = serializer.save()
            serialized_user = WriteUserSerializer(user).data
            return Response(serialized_user, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        serialized_user = UserSerializer(user)
        return Response(status=status.HTTP_200_OK, data=serialized_user.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
