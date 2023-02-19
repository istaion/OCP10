from rest_framework.serializers import ModelSerializer

from projects.models import Project, Issue, Contributor, Comment


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

class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description']
        extra_kwargs = {
            'author': {'read_only': True},
            'issue': {'read_only': True},
            'created_time': {'read_only': True}
        }