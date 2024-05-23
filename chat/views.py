from rest_framework import viewsets
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from .serializers import UserSerializer,GroupSerializer,GroupAddMemberSerializer,GroupCreateSerializer,GroupMessageSerializer,MessageCreateSerializer
from .models import GroupMessage,Group,get_user_model


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by('username')
    serializer_class = UserSerializer
    http_method_names = ['get']

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    http_method_names = ['get']


class GroupCreate(viewsets.ModelViewSet):

    queryset = Group.objects.all().order_by('name')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GroupSerializer
    http_method_names = ['post']

    def create(self, request, format=None):
        serializer = GroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.created_by = request.user
            obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class GroupDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Group.objects.get(id=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        serializer = GroupSerializer(group_obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        print(group_obj)
        serializer = GroupCreateSerializer(instance=group_obj, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            if not obj.created_by:
                obj.created_by = request.user
                obj.save()
            return Response({
                "success": "Group Details Updated", "data": serializer.data
            },
                status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

    def delete(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        group_obj.delete()
        return Response({"success": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class GroupMember(APIView):
    def get_object(self, pk):
        try:
            return Group.objects.get(id=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        serializer = GroupSerializer(group_obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        serializer = GroupAddMemberSerializer(instance=group_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": "Users added/removed successfully",
                "data": serializer.data},
                status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class GroupChat(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Group.objects.get(id=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        group_messages = GroupMessage.objects.filter(group=group_obj).order_by("id")
        if group_messages:
            group_messages = GroupMessageSerializer(group_messages, many=True)
            return Response(group_messages.data)
        return Response({"Message": "No Conversation"})

    def post(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_id=request.user.id, group_id=group_obj.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class MessageLike(APIView):
    def get_object(self, group_id, msg_id):
        try:
            return GroupMessage.objects.get(group_id=group_id, id=msg_id)
        except GroupMessage.DoesNotExist:
            raise Http404

    def get(self, request, group_id, msg_id, format=None):
        message_obj = self.get_object(group_id, msg_id)
        print(message_obj)
        serializer = GroupMessageSerializer(message_obj)
        return Response(serializer.data)

    def post(self, request, group_id, msg_id, format=None):
        message_obj = self.get_object(group_id, msg_id)
        if request.user in message_obj.is_liked.all():
            message_obj.is_liked.remove(request.user.id)
            return Response({"success": "Unliked successfully"},status=status.HTTP_204_NO_CONTENT)
        else:
            message_obj.is_liked.add(request.user.id)
            return Response({"success": "Liked successfully"},status=status.HTTP_204_NO_CONTENT)