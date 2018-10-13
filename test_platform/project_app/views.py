from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from project_app.models import Project


# Create your views here.

@login_required
def project_manage(request):
    username = request.session.get("user", '')
    project = Project.objects.all()
    return render(request, "project_manage.html", {"user": username, "projects": project, "type": "list"})


@login_required
def create_project(request):
    return render(request, "project_manage.html", {"type": "add"})


@login_required
def save_project(request):
    return render(request, "project_manage.html", {"type": "save"})
