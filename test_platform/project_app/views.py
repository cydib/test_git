from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from project_app.models import Project
from .forms import ProjectForm


# Create your views here.

@login_required
def project_manage(request):
    username = request.session.get("user", '')
    project = Project.objects.all()
    return render(request, "project_manage.html", {"user": username, "projects": project, "type": "list"})


@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            print("name", name)
            print("describe", describe)
            Project.objects.create(name=name, describe=describe)
            return HttpResponseRedirect('/manage/project_manage/')
    else:
        form = ProjectForm()
    return render(request, "project_manage.html", {'form': form, "type": "add"})

