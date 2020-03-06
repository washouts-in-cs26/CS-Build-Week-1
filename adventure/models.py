from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(
        max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    # def __repr__(self):
    #     return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
    #     return f"({self.x}, {self.y})"
    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        print("destid", destinationRoomID)
        # setattr(self, f"{direction}_to", int(destinationRoom.id))
        # self.{direction}_to = destinationRoomID
        # destinationRoom."{direction}"_to
        # setattr(destinationRoom, f"{reverse_dir}_to", self)
        try:
            print("try fired!", destinationRoomID)
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
                print('elif n', self.n_to)
            elif direction == "s":
                self.s_to = destinationRoomID
                print('elif n', self.n_to)
            elif direction == "e":
                print('elif e')
                self.e_to = destinationRoomID
            elif direction == "w":
                print('elif w')
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()
    # def items(self):
    #     library = dict()
    #     room_contents = [item for i in Roo]

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Item(models.Model):
    name = models.CharField(max_length=50, default="DEFAULT ITEM")
    description = models.CharField(
        max_length=500, default="DEFAULT DESCRIPTION")
    item_type = models.CharField(max_length=50, default="DEFAULT TYPE")


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.get_or_create(user=instance)
        Token.objects.get_or_create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
