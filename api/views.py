from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import IsPollCreator
from api.serializers import PollSerializer
from polls.models import Poll


class PollListCreateAPIView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class PollDeleteAPIView(generics.DestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (IsPollCreator, )
