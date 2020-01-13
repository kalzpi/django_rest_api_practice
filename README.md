# Airbnb API

REST & GraphQL API of the Airbnb Clone using Django REST Framework and Graphene GraphQL

### API Actions

- [ ] List Rooms
- [ ] Filter Rooms
- [ ] Search By Coords
- [ ] Login
- [ ] Create Account
- [ ] See Room
- [ ] Add Room to Favourites
- [ ] See Favs
- [ ] See Profile
- [ ] Edit Profile

## things that I've learned

1. Serializer Validation
https://www.django-rest-framework.org/api-guide/serializers/#validation

2. Update and Instance
~~~
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.price = validated_data.get("price", instance.price)
        instance.beds = validated_data.get("beds", instance.beds)
        instance.save()
        return instance
~~~
update과 create의 차이. View에서 data와 함께 serializer를 불러올 때 instance를 넘겨주면 update, 안넘겨주면 create이다.
- update
~~~
serializer = CreateRoomSerializer(room, data=request.data, partial=True)
~~~
- create
~~~
serializer = CreateRoomSerializer(data=request.data)
~~~
여기서 partial=true라고 하지않으면 update 시에도 모든 instance에 정의된 모든 data를 넘겨주어야 한다.
instance란 Room, User등과 같은 django object를 말한다.
