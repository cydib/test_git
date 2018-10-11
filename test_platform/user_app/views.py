from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from user_app.models import Project, Module


# Create your views here.

def index(request):
    return render(request, "index.html")


def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if username == "" or password == "":
            return render(request, "index.html", {"error": "用户名或密码不能为空"})
        else:
            user = auth.authenticate(
                username=username, password=password)

            if user is not None:
                auth.login(request, user)  # 记录用户登录状态
                request.session['user'] = username
                return HttpResponseRedirect('/project_manage/')
            else:
                return render(request, "index.html", {"error": "用户名或密码错误"})


@login_required
def project_manage(request):
    username = request.session.get("user", '')
    project = Project.objects.all()
    return render(request, "project_manage.html", {"user": username, "projects": project})


def logout(request):
    auth.logout(request)
    respone = HttpResponseRedirect("/")
    return respone
