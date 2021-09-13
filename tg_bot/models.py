from django.db import models


class User(models.Model):
    # User info
    telegram_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    tag = models.CharField(max_length=200, blank=True)

    # User in-game stuff
    correct_answers = models.IntegerField(default=0)
    game_in_process = models.BooleanField(default=False)
    current_game_id = models.IntegerField(default=-1)


class GroupChat(models.Model):
    telegram_id = models.CharField(max_length=100)
    game_in_process = models.BooleanField(default=False)
    game_id = models.IntegerField(blank=True)
    users = models.ManyToManyField(User)



