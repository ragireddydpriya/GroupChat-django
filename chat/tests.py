from django.test import TestCase,Client
from rest_framework.authtoken.models import Token
from chat.apps import ChatConfig
from django.urls import reverse
from .models import Group, GroupMessage
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()

class ObjectsCreation(object):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="user1",email="user1@gmail.com",is_superuser=True,is_staff=True,)
        self.user1.set_password('secret')
        self.user1.save()
        self.token1 = Token.objects.get(user=self.user1)
        self.user2 = User.objects.create_user(username="user2",email="user2@gmail.com",is_superuser=False,)
        self.user2.set_password('secret2')
        self.user2.save()
        self.token2 = Token.objects.get(user=self.user2)
        self.group1 = Group.objects.create(name="Group 1", created_by=self.user1)
        self.group2 = Group.objects.create(name="Group 2", created_by=self.user1)
        self.group3 = Group.objects.create(name="Group 3")
        self.group_message1 = GroupMessage.objects.create(msg="Hi", group=self.group1, created_by=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)


class TestChat(ObjectsCreation, TestCase):
    def test_app_file(self):
        self.assertEqual(ChatConfig.name, "chat")

    def test_groupCreate(self):
        self.assertTrue(self.client.login(username="user1", password="secret"))
        response = self.client.post(reverse("groupcreate-list"), data={"name": "Test Group 1",})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse("groupcreate-list"), data={})
        self.assertEqual(response.status_code, 409)

    def test_groupList(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.get(reverse("grouplist-list"))
        self.assertEqual(response.status_code, 200)

    def test_groupDetail(self):
        self.assertTrue(self.client.login(username="user1", password="secret"))
        response = self.client.get(reverse("GroupDetail", kwargs={'pk': self.group2.id}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("GroupDetail", kwargs={'pk': 55}))
        self.assertEqual(response.status_code, 404)
        response = self.client.put(reverse("GroupDetail", kwargs={'pk': self.group2.id}), data={"name": "Group 2",})
        self.assertEqual(response.status_code, 204)
        response = self.client.put(reverse("GroupDetail", kwargs={'pk': self.group3.id}), data={"name": "Group 3",})
        self.assertEqual(response.status_code, 204)
        response = self.client.put(reverse("GroupDetail", kwargs={'pk': self.group2.id}), data={"username": "user2"})
        self.assertEqual(response.status_code, 409)
        response = self.client.delete(reverse("GroupDetail", kwargs={'pk': self.group2.id}))
        self.assertEqual(response.status_code, 204)

    def test_groupMember(self):
        response = self.client.get(reverse("GroupMember", kwargs={'pk': self.group1.id}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("GroupMember", kwargs={'pk': 44}))
        self.assertEqual(response.status_code, 404)
        response = self.client.put(reverse("GroupMember", kwargs={'pk': self.group1.id}), data={"members": [self.user1.id, self.user2.id]})
        self.assertEqual(response.status_code, 204)
        response = self.client.put(reverse("GroupMember", kwargs={'pk': self.group1.id}), data={"members": [self.user1.id, 22]})
        self.assertEqual(response.status_code, 409)

    def test_groupChat(self):
        self.assertTrue(self.client.login(username="user1", password="secret"))
        response = self.client.get(reverse("GroupChat", kwargs={'pk': self.group1.id}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("GroupChat", kwargs={'pk': self.group2.id}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("GroupChat", kwargs={'pk': 44}))
        self.assertEqual(response.status_code, 404)
        response = self.client.post(reverse("GroupChat", kwargs={'pk': self.group1.id}), data={"msg": "Hi I am user1"})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse("GroupChat", kwargs={'pk': self.group1.id}), data={})
        self.assertEqual(response.status_code, 409)

    def test_MessageLike(self):
        response = self.client.get(reverse("MessageLike", kwargs={'group_id': self.group1.id, 'msg_id': self.group_message1.id}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("MessageLike", kwargs={'group_id': self.group1.id, 'msg_id': self.group_message1.id}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("MessageLike", kwargs={'group_id': 123, 'msg_id': self.group_message1.id}))
        self.assertEqual(response.status_code, 404)
        response = self.client.post(reverse("MessageLike", kwargs={'group_id': self.group1.id, 'msg_id': self.group_message1.id}))
        self.assertEqual(response.status_code, 204)
        response = self.client.post(reverse("MessageLike", kwargs={'group_id': self.group1.id, 'msg_id': self.group_message1.id}))
        self.assertEqual(response.status_code, 204)
