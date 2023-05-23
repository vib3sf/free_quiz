from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import IsPollCreator
from api.serializers import PollSerializer, VoteSerializer
from polls.models import Poll, Vote


class PollListCreateAPIView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class PollDeleteAPIView(generics.DestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (IsPollCreator, )


class VoteListCreateAPIVIew(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (IsPollCreator, )
