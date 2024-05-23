from rest_framework import serializers

from .models import GroupMessage,Group


from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('username','email')



class GroupSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True,default=serializers.CurrentUserDefault())

    class Meta:
        model = Group
        fields = ('id','name','description','members','created_by','created_on')



class GroupCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('name','description','members')
        extra_kwargs = {'members': {'required': False}}

    def create(self, validated_data):
        group = super(GroupCreateSerializer, self).create(validated_data)
        group.save()
        return group


class GroupAddMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['members']
        extra_kwargs = {'members': {'required': False}}


class GroupMessageSerializer(serializers.ModelSerializer):
    is_liked = UserSerializer(read_only=True, many=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = GroupMessage
        fields=['id','msg','group','is_liked','created_by','created_on']


class MessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMessage
        fields = ['msg',]
        extra_kwargs = {'group': {'required': False}}