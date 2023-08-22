from rest_framework import serializers
from .models import MyUser, Interest
from rest_framework.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(write_only=True, required=True)
    interests = serializers.SlugRelatedField(queryset=Interest.objects.all(), many=True, slug_field="name")


    class Meta:
        model = MyUser
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "interests"
        ]
        extra_kwargs = {"first_name": {"required": False},
                        "last_name": {"required": False},
                        }
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        user = MyUser(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        if validated_data.get("first_name"):
            user.first_name = validated_data.get("first_name")
        if validated_data.get("last_name"):
            user.first_name = validated_data.get("last_name") 
        user.set_password(validated_data["password"])
        user.save()
        user.interests.set(validated_data["interests"])
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    
    interests = serializers.SlugRelatedField(queryset=Interest.objects.all(), many=True, required=False, slug_field="name")
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model=MyUser
        fields=[
            "username", 
            "email", 
            "first_name", 
            "last_name", 
            "interests", 
            "image", 
            "description", 
            "links"
        ]