from rest_framework import status, response
from rest_framework.viewsets import ReadOnlyModelViewSet
from projects.models import Project, Issue, Contributor
from projects.serializers import ProjectSerializer, IssueSerializer, ProjectIdSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


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
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectIdSerializer

    def retrieve (self, request, *args, **kwargs):
        obj = get_object_or_404(Project, id=kwargs['project_id'])
        project = ProjectIdSerializer(obj, many=False)
        return response.Response(project.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Project, id=kwargs['project_id'])
        serializer = ProjectIdSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(Project, id=kwargs['project_id'])
        title = obj.title
        self.perform_destroy(obj)
        message = 'Vous avez supprimé le projet :' + str(title)
        return response.Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)

