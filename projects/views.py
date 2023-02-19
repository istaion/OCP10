from rest_framework import status, response
from rest_framework.viewsets import ReadOnlyModelViewSet
from projects.models import Project, Issue, Contributor, Comment
from projects.serializers import (ProjectSerializer, IssueSerializer, ProjectIdSerializer,
                                  ContributorsSerializer, CommentsSerializer)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from authentication.permissions import ObjectPermission
from authentication.models import User


# /projects/
class ProjectsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    # gets list of Projects
    def list(self, request, *args, **kwargs):
        qs = Project.objects.filter(contributors=request.user)
        serializer = self.serializer_class(qs, many=True)
        return response.Response(serializer.data,
                                 status=status.HTTP_200_OK)

    # creates a new project
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            project = serializer.save(author=request.user)
            contributor = Contributor.objects.create(project=project,
                                                     contributor=request.user,
                                                     role='author')
            contributor.save()
            return response.Response(serializer.data,
                                     status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors,
                                     status=status.HTTP_400_BAD_REQUEST)

class ProjectIdView(ModelViewSet):
    permission_classes = [IsAuthenticated, ObjectPermission]
    queryset = Project.objects.all()
    serializer_class = ProjectIdSerializer

    def retrieve (self, request, *args, **kwargs):
        obj = get_object_or_404(Project, id=kwargs['project_id'])
        project = self.serializer_class(obj, many=False)
        return response.Response(project.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Project, id=kwargs['project_id'])
        self.check_object_permissions(self.request, obj)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(Project, id=kwargs['project_id'])
        self.check_object_permissions(self.request, obj)
        title = obj.title
        self.perform_destroy(obj)
        message = 'Vous avez supprimé le projet :' + str(title)
        return response.Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)

class ContributorsView(ModelViewSet):
    permission_classes = [IsAuthenticated, ObjectPermission]
    queryset = Contributor.objects.all()
    serializer_class = ContributorsSerializer

    def list(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['project_id'])
        qs = Contributor.objects.filter(project=project)
        serializer = self.serializer_class(qs, many=True)
        return response.Response(serializer.data,
                                 status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        project = get_object_or_404(Project, id=kwargs['project_id'])
        self.check_object_permissions(self.request, project)
        if serializer.is_valid():
            serializer.save(project=project, role='contributor')
            return response.Response(serializer.data,
                                     status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors,
                                     status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['project_id'])
        self.check_object_permissions(self.request, project)
        user = get_object_or_404(User, id=kwargs['user_id'])
        contributor = Contributor.objects.filter(project=project).filter(contributor=user)
        name = user.username
        self.perform_destroy(contributor)
        message = 'L\'utilisateur :' + str(name) + 'ne fait plus parti du projet.'
        return response.Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)


class IssuesView(ModelViewSet):
    permission_classes = [IsAuthenticated, ObjectPermission]
    serializer_class = IssueSerializer

    def list(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['project_id'])
        qs = Issue.objects.filter(project=project)
        serializer = self.serializer_class(qs, many=True)
        return response.Response(serializer.data,
                                 status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['project_id'])
        """get the assignee user and controll if he is a contributor :"""
        if 'assignee' in kwargs:
            assignee = get_object_or_404(User, id=kwargs['assignee'])
            if not Contributor.objects.filter(project=project).filter(contributor=assignee).exists():
                name = assignee.username
                message = 'L\'utilisateur :' + str(name) + 'ne fait pas parti du projet et ne peut être assigné.'
                return response.Response({'message': message},
                                         status=status.HTTP_200_OK)
        else:
            assignee = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, project=project, assignee=assignee)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Issue, id=kwargs['issue_id'])
        self.check_object_permissions(self.request, obj)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(Issue, id=kwargs['issue_id'])
        self.check_object_permissions(self.request, obj)
        title = obj.title
        self.perform_destroy(obj)
        message = 'Vous avez supprimé le problème :' + str(title)
        return response.Response({'message': message},
                                 status=status.HTTP_204_NO_CONTENT)


class CommentView(ModelViewSet):
    permission_classes = [IsAuthenticated, ObjectPermission]
    serializer_class = CommentsSerializer

    def list(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs['issue_id'])
        qs = Comment.objects.filter(issue=issue)
        serializer = self.serializer_class(qs, many=True)
        return response.Response(serializer.data,
                                 status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs['issue_id'])
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, issue=issue)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
