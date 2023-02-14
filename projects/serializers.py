from rest_framework.serializers import ModelSerializer

from projects.models import Project, Issue


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'type']


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project', 'status', 'created_time']


class ProjectIdSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'id', 'author']
        extra_kwargs = {
            'id': {'read_only': True},
            'author': {'read_only': True}
        }