from rest_framework.serializers import ModelSerializer

from projects.models import Project, Issue, Contributor, Comment


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'author': {'read_only': True},
            'created_time': {'read_only': True},
            'project': {'read_only': True}
        }

class ProjectIdSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'author': {'read_only': True}
        }

class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'project': {'read_only': True},
            'role': {'read_only': True}
        }

class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comment
        '__all__'
        extra_kwargs = {
            'author': {'read_only': True},
            'issue': {'read_only': True},
            'created_time': {'read_only': True}
        }