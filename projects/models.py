from django.db import models
from django.conf import settings


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    type = models.CharField(max_length=128)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributor', related_name='contributions')


class Contributor(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)

    class Meta:
        unique_together = ('contributor', 'project')


class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=128)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=128)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.TextField(max_length=2048)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
