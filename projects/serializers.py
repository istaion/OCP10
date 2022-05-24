from rest_framework.serializers import ModelSerializer

from projects.models import Project, Issue


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'contributors']


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project', 'status', 'created_time']

