from rest_framework.serializers import ModelSerializer

from projects.models import Project, Issue, Contributor


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'type']


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'status', 'assignee']
        extra_kwargs = {
            'id': {'read_only': True},
            'author': {'read_only': True},
            'created_time': {'read_only': True},
            'project': {'read_only': True}
        }

class ProjectIdSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'id', 'author']
        extra_kwargs = {
            'id': {'read_only': True},
            'author': {'read_only': True}
        }

class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'contributor', 'project', 'role']
        extra_kwargs = {
            'id': {'read_only': True},
            'project': {'read_only': True},
            'role': {'read_only': True}
        }