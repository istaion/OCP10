from projects.models import Project, Issue, Contributor
from rest_framework.permissions import BasePermission

class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if Contributor.objects.filter(contributor=request.user).filter(project=view.kwargs['project_id']).exists():
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in ("PUT", "DELETE", "POST"):
            return obj.author == request.user
        else:
            return False