from django.contrib.auth.models import Group
from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request
#from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from .serializers import GroupSerializer


@api_view()
def hello_world_view(request: Request) -> Response:

    """API подразумевает возвращение json."""
    return Response({'message': 'Hello world'})

# class GroupsListView(GenericAPIView, ListModelMixin):
#
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#
#     def get(self, request: Request) -> Response:
#         return self.list(request)

class GroupsListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

