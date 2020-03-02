from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

# class Room(models.Model):
    # title = models.CharField(max_length=50, default="DEFAULT TITLE")
    # description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    # n_to = models.IntegerField(default=0)
    # s_to = models.IntegerField(default=0)
    # e_to = models.IntegerField(default=0)
    # w_to = models.IntegerField(default=0)
   
    # def connectRooms(self, destinationRoom, direction):
    #     destinationRoomID = destinationRoom.id
    #     try:
    #         destinationRoom = Room.objects.get(id=destinationRoomID)
    #     except Room.DoesNotExist:
    #         print("That room does not exist")
    #     else:
    #         if direction == "n":
    #             self.n_to = destinationRoomID
    #         elif direction == "s":
    #             self.s_to = destinationRoomID
    #         elif direction == "e":
    #             self.e_to = destinationRoomID
    #         elif direction == "w":
    #             self.w_to = destinationRoomID
    #         else:
    #             print("Invalid direction")
    #             return
    #         self.save()
class Room(models.Model):
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = models.IntegerField(default=0)
        self.s_to = models.IntegerField(default=0)
        self.e_to = models.IntegerField(default=0)
        self.w_to = models.IntegerField(default=0)
        self.x = x
        self.y = y
    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"
    def connect_rooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", destinationRoom)
        setattr(destinationRoom, f"{reverse_dir}_to", self)
        self.save()
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")
    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


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

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()





