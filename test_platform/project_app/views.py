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
            Project.objects.create(name=name, describe=describe)
            return HttpResponseRedirect('/manage/project_manage/')
    else:
        form = ProjectForm()
    return render(request, "project_manage.html", {'form': form, "type": "add"})


@login_required
def edit_project(request, pid):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            Project.objects.select_for_update().filter(id=pid).update(name=name, describe=describe)
            return HttpResponseRedirect('/manage/project_manage/')
    else:
        if pid:
            form = ProjectForm(instance=Project.objects.get(id=pid))
        else:
            form = ProjectForm()
    return render(request, "project_manage.html", {'form': form, "pid": pid, "type": "edit"})


@login_required
def del_project(request, pid):
        Project.objects.get(id=pid).delete()
        return HttpResponseRedirect('/manage/project_manage/')