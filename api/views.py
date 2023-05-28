from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsPollCreator
from api.serializers import PollSerializer, VoteListSerializer
from polls.models import Poll, Vote


class PollListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PollSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Poll.objects.filter(creator=self.request.user) if 'poll_id' not in self.kwargs \
            else Poll.objects.filter(id=self.kwargs['poll_id'], creator=self.request.user)


class PollDeleteAPIView(generics.DestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (IsPollCreator, )


class VoteCreateAPIVIew(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteListSerializer
    permission_classes = (IsPollCreator, )
