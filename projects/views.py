from rest_framework import status, response
from rest_framework.viewsets import ReadOnlyModelViewSet
from projects.models import Project, Issue, Contributor
from projects.serializers import ProjectSerializer, IssueSerializer, ProjectIdSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


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
        if Project.objects.get(id=kwargs['project_id']):
            res = Project.objects.get(id=kwargs['project_id'])
            project = ProjectIdSerializer(res, many=False)
            return response.Response(project.data,
                            status=status.HTTP_200_OK)
