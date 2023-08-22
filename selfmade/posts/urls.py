from django.urls import path, include
# from .views import PostCreateView, PostDetailView, PostListView
from .views import PostView, CommentView, VoteViewSet, TagPostsView, CommentVoteViewSet
from rest_framework import routers
router = routers.DefaultRouter()
router.register("posts", PostView, basename="posts")
router.register(r"votes", VoteViewSet)
router.register(r"comments_votes", CommentVoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("comments/<int:pk>", CommentView.as_view(), name="comments"),
    path("tags/<str:tags>", TagPostsView.as_view(), name="search"),
]
# urlpatterns = [
#     path("add_post", PostCreateView.as_view(), name="add_post"),
#     path("<int:pk>", PostDetailView.as_view(), name="post_detail"),
#     path("", PostListView.as_view(), name="post_list")
# ]
