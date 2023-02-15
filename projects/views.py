from rest_framework import status, response
from rest_framework.viewsets import ReadOnlyModelViewSet
from projects.models import Project, Issue, Contributor
from projects.serializers import ProjectSerializer, IssueSerializer, ProjectIdSerializer, ContributorsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from authentication.permissions import ProjectPermission


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
    permission_classes = [IsAuthenticated, ProjectPermission]
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
    permission_classes = [IsAuthenticated, ProjectPermission]
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