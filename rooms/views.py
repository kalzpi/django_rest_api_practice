from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, CreateRoomSerializer


@api_view(["GET", "POST"])
def rooms_view(request):
    if request.method == "GET":
        rooms = Room.objects.all()[:5]
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = CreateRoomSerializer(data=request.data)
        if serializer.is_valid():
            # 아래를 보면 serializer.save를 room에 할당하고 있다.
            # 이는 Room create 직후 생성한 Room을 response로 돌려주기 위함인데, mandatory는 아니다.
            # 만약 생성한 Room을 곧바로 보낼 필요가 없다면 Response에서 data항목 제거, serializer.save(user=request.user) 만 하면 된다.
            room = serializer.save(user=request.user)
            room_serializer = ReadRoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        pass


class RoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()[:5]
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = CreateRoomSerializer(data=request.data)
        if serializer.is_valid():
            # 아래를 보면 serializer.save를 room에 할당하고 있다.
            # 이는 Room create 직후 생성한 Room을 response로 돌려주기 위함인데, mandatory는 아니다.
            # 만약 생성한 Room을 곧바로 보낼 필요가 없다면 Response에서 data항목 제거, serializer.save(user=request.user) 만 하면 된다.
            room = serializer.save(user=request.user)
            room_serializer = ReadRoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = ReadRoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                # Create과 update의 차이: serializer initialize때 object를 instance로 주면 update, 안주면 create
                serializer = CreateRoomSerializer(room, data=request.data, partial=True)
                if serializer.is_valid():
                    room = serializer.save()
                    return Response(data=room, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                room.delete()
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
