from projects.models import Project, Issue, Contributor
from rest_framework.permissions import BasePermission

class ObjectPermission(BasePermission):
    def has_permission(self, request, view):
        if Contributor.objects.filter(contributor=request.user).filter(project=view.kwargs['project_id']).exists():
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


