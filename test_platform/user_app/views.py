from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


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
                return HttpResponseRedirect('/manage/project_manage/')
            else:
                return render(request, "index.html", {"error": "用户名或密码错误"})


def logout(request):
    auth.logout(request)
    respone = HttpResponseRedirect("/")
    return respone
