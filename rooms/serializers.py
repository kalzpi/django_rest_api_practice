from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ("modified",)
        read_only_fields = ("user", "id", "created")

    def validate(self, data):

        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
            beds = data.get("beds", self.instance.beds)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
            beds = data.get("beds")

        if beds > 100:
            raise serializers.ValidationError("That house is too big!")
        if check_in == check_out:
            raise serializers.ValidationError(
                "Seriously? There must be no time to prepare room!"
            )
        return data

    def get_is_fav(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            return obj in user.favs.all()
        return False
