# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import re

EMAIL_REGEX = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

class UserManager(models.Manager):

    def validate(self, data):
        response = []
        errors = 0

        # check first_name
        if data['first_name'].isalpha() and len(data['first_name']) > 1:
            response.append([True, '', ''])
        else:
            errors += 1
            response.append([False, 'First name must be all letters and at least 2 characters', 'first_name'])

        # check last_name
        if data['last_name'].isalpha() and len(data['last_name']) > 1:
            response.append([True, '', ''])
        else:
            errors += 1
            response.append([False, 'Last name must be all letters and at least 2 characters', 'last_name'])

        # check email
        if EMAIL_REGEX.match(data['email']):
            try:
                self.get(email = data['email'])
                errors += 1
                response.append([False, 'Please enter a different email', 'email'])
            except ObjectDoesNotExist:
                response.append([True, '', ''])
        else:
            errors += 1
            response.append([False, 'Must be a valid Email format', 'email'])

        # check password
        if len(data['password']) > 7:
            if data['password'] == data['c_password']:
                response.append([True, '', ''])
            else:
                errors += 1
                response.append([False, 'Passwords must match', 'c_password'])
        else:
            errors += 1
            response.append([False, 'Password must be at least 8 characters', 'password'])

        # check for any errors and return approriate message if so, no errors then just return successful message
        if errors > 0:
            return response
        return [True, '', '']

    def login(self, data):
        # first check if information entered is valid before we ping db
        if EMAIL_REGEX.match(data['email']) and len(data['password'])>7:
            # if valid then check if credentials match those stored in db
            try:
                if self.get(email = data['email']):
                    if self.get(email = data['email']).password == data['password']:
                        return [True, '', '']
                    else:
                        return [False, 'Incorrect email or password', 'login-error']
            except:
                return [False, 'Incorrect email or password', 'login-error']
        # if info is not valid then just return error and not ping db
        else:
            return [False, 'Incorrect email or password', 'login-error']

class User(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name
