from rest_framework import serializers 
from .models import Post, Comment, Vote
from taggit.serializers import TaggitSerializer, TagListSerializerField
from users.models import MyUser
from rest_framework.exceptions import ValidationError



class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    author = serializers.SlugRelatedField("username", queryset=MyUser.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "description", "image", "author", "tags", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    
    username = serializers.SlugRelatedField("username", queryset=MyUser.objects.all(), required=False)

    class Meta:
        model=Comment
        fields=["post", "username", "text", "created_date"]
        extra_kwargs={"post": {"required": False}}


class VoteSerializer(serializers.ModelSerializer):

    owner = serializers.SlugRelatedField("username", read_only=True)

    class Meta:
        model=Vote
        fields=["owner", "post"]


class CommentVoteSerializer(serializers.ModelSerializer):

    owner = serializers.SlugRelatedField("username", read_only=True)

    class Meta:
        model=Vote
        fields=["owner", "comment", "direction"]

