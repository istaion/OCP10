from django.db import models
from django.conf import settings
from authentication.models import User

PROJECT_CHOICES = (('Back-end', 'Back-end'), ('Front-end', 'Front-end'), ('iOS', 'iOS',), ('Android', 'Android'))


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    type = models.CharField(choices=PROJECT_CHOICES, max_length=128)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributor', related_name='contributions')


ROLE_CHOICES = (('author', 'author'), ('contributor', 'contributor'))


class Contributor(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES, max_length=128)

    class Meta:
        unique_together = ('contributor', 'project')


PRIORITY_CHOICES = (('FAIBLE', 'FAIBLE'), ('MOYENNE', 'MOYENNE'), ('ELEVE', 'ELEVE',))
TAG_CHOICES = (('BUG', 'BUG'), ('AMELIORATION', 'AMELIORATION'), ('TACHE', 'TACHE'))
STATUS_CHOICES = (('A faire', 'A faire'), ('En cours', 'En cours'), ('Terminé', 'Terminé'))


class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=2048)
    tag = models.CharField(choices=TAG_CHOICES, max_length=128)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=128)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=128)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee_user = models.ForeignKey(
        to=User, default=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignee')
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=2048)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
