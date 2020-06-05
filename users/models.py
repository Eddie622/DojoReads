from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"

        if len(postData['name']) < 3:
            errors["name"] = "Name should be at least 3 characters"
        if len(postData['alias']) < 3:
            errors["alias"] = "Alias should be at least 3 characters"
        if len(postData['pwd']) < 8:
            errors["pwd"] = "Password should be at least 8 characters"
        if postData['pwd'] != postData['confirm_pwd']:
            errors['confrim_pwd'] = "Passwords do not match"
        
        users = User.objects.all()
        for user in users:
            if postData['email'] == user.email:
                errors['email'] = "email is taken"

        return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
