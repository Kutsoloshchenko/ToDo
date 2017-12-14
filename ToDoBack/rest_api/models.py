"""Module with all models that correspond to data base tables """

from django.db import models


class User(models.Model):
    """User model"""
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=250)

    class Meta:
        ordering = ('id',)


class Project(models.Model):
    """Projects model"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    color = models.CharField(max_length=25)

    class Meta:
        ordering = ('id',)


class Task(models.Model):
    """Tasks model"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    state = models.CharField(max_length=25, default="In Progress")
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    priority = models.IntegerField()

    class Meta:
        ordering = ('id',)