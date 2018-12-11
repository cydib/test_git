from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from project_app.models import Project
from project_app.forms import ProjectForm


# Create your views here.

@login_required
def project_manage(request):
    username = request.session.get("user", '')
    project = Project.objects.all()
    paginator = Paginator(project, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)

    return render(request, "project_manage.html", {"user": username, "projects": contacts, "type": "list"})


@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            status = form.cleaned_data['status']
            Project.objects.create(name=name, describe=describe, status=status)
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
            status = form.cleaned_data['status']
            Project.objects.select_for_update().filter(id=pid).update(name=name, describe=describe, status=status)
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
