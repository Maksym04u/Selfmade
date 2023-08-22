from rest_framework import viewsets, generics, permissions, pagination, views, mixins, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .serializers import PostSerializer, CommentSerializer, VoteSerializer, CommentVoteSerializer
from .models import Post, Comment, Vote, CommentVote
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from rest_framework.exceptions import ValidationError



# class PostCreateView(generics.CreateAPIView):

#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):

#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsOwnerOrReadOnly]
    
#     # def get_queryset(self):
#     #     post_id = self.kwargs["pk"]
#     #     return Post.objects.filter(pk=post_id)

# class PostListView(generics.ListAPIView):

#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [permissions.AllowAny]
#     pagination_class=pagination.PageNumberPagination


class PostView(viewsets.ModelViewSet):
    serializer_class=PostSerializer
    queryset = Post.objects.all()
    pagination_class=pagination.PageNumberPagination
    permission_classes= [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentView(generics.ListCreateAPIView):
    serializer_class=CommentSerializer
    queryset=Comment.objects.all()
    pagination_class=pagination.PageNumberPagination
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        serializer.save(post=post, username=self.request.user) 
    
    def get_queryset(self):
        id = self.kwargs['pk']
        post = Post.objects.get(pk=id)
        return Comment.objects.filter(post=post)
    

class VoteViewSet(viewsets.ModelViewSet):
    
    serializer_class=VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Vote.objects.all()

    @action(detail=False, methods=['post'])
    def toggle_like(self, request):
        post_id = request.data.get("post")
        user = self.request.user    

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        existing_vote = Vote.objects.filter(post=post, owner=user).first()

        if existing_vote:
            existing_vote.delete()
            return Response({'message': 'Like removed'}, status=status.HTTP_204_NO_CONTENT)
        else:
            Vote.objects.create(post=post, owner=user)
            return Response({'message': 'Liked'}, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        if not Post.objects.filter(pk = self.kwargs["pk"]):
            return Response({"message": "post not found"}, status=status.HTTP_404_NOT_FOUND)
        total = Vote.objects.filter(post=self.kwargs["pk"]).count()
        return Response({"likes": total})

# class CreateDestroyRetrieveAPIView(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    

# class VoteView(CreateDestroyRetrieveAPIView):

#     serializer_class=VoteSerializer
#     queryset=Vote.objects.all()
#     permission_classes=[permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         post = get_object_or_404(Post, pk=self.kwargs["pk"])
#         if Vote.objects.filter(post=post, owner=self.request.user):
#             self.perform_destroy(Vote.objects.get(post=post, owner=self.request.user))
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             serializer.save(post=post, owner=self.request.user)  

#     def get_object(self):
#         post = get_object_or_404(Post, pk=self.kwargs["pk"])
#         owner = self.request.user
#         vote = get_object_or_404(Vote, post=post, owner=owner)
#         return vote
    
#     def retrieve(self, request, *args, **kwargs):
#         total = Vote.objects.filter(post=self.kwargs["pk"]).count()
#         return Response({"votes": total})
    


class TagPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tags = None
        try:
            tags = Tag.objects.get(name=self.kwargs["tags"])
        finally:
            return Post.objects.filter(tags=tags)
    
class CommentVoteViewSet(viewsets.ModelViewSet):

    serializer_class = CommentVoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = CommentVote.objects.all()

    @action(methods=["post"], detail=True)
    def like_dislike(self, request, *arg, **kwargs):
        owner = self.request.user
        comment = get_object_or_404(Comment, pk=self.kwargs["pk"])
        direction = request.data.get("direction")
        if not direction in [-1, 1]: 
            raise ValidationError("This value is not acceptible")
        
        existing_vote = CommentVote.objects.filter(owner=owner, comment=comment).first()
        if existing_vote and existing_vote.direction != direction:
            existing_vote.direction = direction
            existing_vote.save()
            return Response({"message": "Vote changed"}, status=status.HTTP_200_OK)
        elif existing_vote and existing_vote.direction == direction:
            existing_vote.delete()
            return Response({"message": "Vote deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            CommentVote.objects.create(owner=owner, comment=comment, direction=direction)
            return Response({"message": "Vote created"}, status=status.HTTP_201_CREATED)
        
    def retrieve(self, request, *args, **kwargs):
        if not Comment.objects.filter(pk = self.kwargs["pk"]):
            return Response({"message": "comment not found"}, status=status.HTTP_404_NOT_FOUND)
        total = CommentVote.objects.filter(comment=self.kwargs["pk"]).count()
        return Response({"difference": total})

