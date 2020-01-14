import jwt
from rest_framework import permissions
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from .permissions import IsSelf
from rooms.serializers import RoomSerializer
from rooms.models import Room


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        elif self.action == "create":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def search(self, request):
        username = request.GET.get("username", None)
        first_name = request.GET.get("first_name", None)
        last_name = request.GET.get("last_name", None)
        email = request.GET.get("email", None)
        is_staff = request.GET.get("is_staff", None)
        date_joined = request.GET.get("date_joined", None)
        superhost = request.GET.get("superhost", None)

        filter_kwargs = {}
        if username is not None:
            filter_kwargs["username__startswith"] = username
        if first_name is not None:
            filter_kwargs["first_name__startswith"] = first_name
        if last_name is not None:
            filter_kwargs["last_name__startswith"] = last_name
        if email is not None:
            filter_kwargs["email__startswith"] = email
        if is_staff is not None:
            filter_kwargs["is_staff__isnull"] = is_staff
        if date_joined is not None:
            filter_kwargs["date_joined__date__gt"] = date_joined
        if superhost is not None:
            filter_kwargs["superhost__isnull"] = superhost

        paginator = self.paginator
        try:
            users = User.objects.filter(**filter_kwargs)
        except ValueError:
            users = User.objects.all()
        results = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


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
