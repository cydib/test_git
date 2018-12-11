from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from project_app.models import Module
from project_app.forms import ModuleForm


# Create your views here.

@login_required
def module_manage(request):
    username = request.session.get("user", '')
    module = Module.objects.all()
    paginator = Paginator(module, 10)
    page = request.GET.get('page')

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "module_manage.html", {"user": username, "modules": contacts, "type": "list"})


@login_required
def add_module(request):
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            project = form.cleaned_data['project']
            Module.objects.create(name=name, describe=describe, project=project)
            return HttpResponseRedirect('/manage/module_manage/')
    else:
        form = ModuleForm()
    return render(request, "module_manage.html", {'form': form, "type": "add"})


@login_required
def edit_module(request, mid):
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            project = form.cleaned_data['project']
            Module.objects.select_for_update().filter(id=mid).update(name=name, describe=describe, project=project)
            return HttpResponseRedirect('/manage/module_manage/')
    else:
        if mid:
            form = ModuleForm(instance=Module.objects.get(id=mid))
    return render(request, "module_manage.html", {'form': form, "mid": mid, "type": "edit"})


@login_required
def del_module(request, mid):
        Module.objects.get(id=mid).delete()
        return HttpResponseRedirect('/manage/module_manage/')