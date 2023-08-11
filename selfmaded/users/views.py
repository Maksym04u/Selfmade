from .permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, ProfileSerializer
from .models import MyUser



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    


class ProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    
    def get_queryset(self):
        user_id = self.kwargs["pk"]
        return MyUser.objects.filter(pk=user_id)