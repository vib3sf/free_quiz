from rest_framework import generics

from api.serializers import PollSerializer
from polls.models import Poll


class PollListCreateAPIView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollDeleteAPIView(generics.DestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

