from projects.models import Contributor
from rest_framework.permissions import BasePermission

class ObjectPermission(BasePermission):
    def has_permission(self, request, view):
        # Control if the request user is a contributor of the project
        if Contributor.objects.filter(contributor=request.user).filter(project=view.kwargs['project_id']).exists():
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Control if the request user is the author of the object (project, issue or comment)
        return obj.author == request.user


