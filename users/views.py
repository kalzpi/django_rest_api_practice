import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from rooms.serializers import RoomSerializer
from rooms.models import Room


class UsersView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(UserSerializer(new_user).data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serialized_user = UserSerializer(request.user)
        return Response(data=serialized_user.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        print(serializer.is_valid())
        if serializer.is_valid():
            user = serializer.save()
            serialized_user = UserSerializer(user).data
            return Response(serialized_user, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

    def put(self, request):
        pk = request.data.get("pk", None)
        user = request.user
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response(status.HTTP_200_OK)
            except Room.DoesNotExist:
                pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        serialized_user = UserSerializer(user)
        return Response(status=status.HTTP_200_OK, data=serialized_user.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        encoded_jwt = jwt.encode(
            {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
        )
        return Response(data={"token": encoded_jwt})
    else:
        return Response(status.HTTP_400_BAD_REQUEST)
