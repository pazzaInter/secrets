# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import Count
from ..login.models import User

class SecretManager(models.Manager):
    def new_secret(self, *data):
        if len(data[0]) >0:
            self.create(secret = data[0], user_id = User.objects.get(email = data[1]))
            return True
        else:
            return False
    def popular(self):
        return self.annotate(num_likes=Count('secret_like')).order_by('num_likes').reverse()

    def recent(self):
        return self.all().order_by('created_at').reverse()[:5]

class LikeManager(models.Manager):
    def liked(self, *data):
        self.create(user_id=User.objects.get(email=data[0]), secret_id=Secret.objects.get(id=data[1]))

class Secret(models.Model):
    secret = models.TextField()
    user_id = models.ForeignKey(User, related_name='secret')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = SecretManager()

    # this will return all User objects for the secret passed in
    def secretlikes(self):
        return User.objects.filter(user_like__secret_id=self)


class Like(models.Model):
    user_id = models.ForeignKey(User, related_name='user_like')
    secret_id = models.ForeignKey(Secret, related_name='secret_like')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = LikeManager()
