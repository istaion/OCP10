from django.contrib import admin
from projects.models import Project, Contributor, Issue


class ProjectAdmin(admin.ModelAdmin):

    list_display = ('title', 'type')


class ContributorAdmin(admin.ModelAdmin):

    list_display = ('contributor', 'project', 'role')


class IssueAdmin(admin.ModelAdmin):

    list_display = ('title', 'status')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
