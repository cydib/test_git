from django.urls import path
from interface_app.views import testcase_views, testcase_api

urlpatterns = [
    path('case_manage/', testcase_views.case_manage),
    path('add_case/', testcase_views.add_case),
    path('debug_case/', testcase_views.debug_case),
    path('edit_case/<int:cid>/', testcase_views.edit_case),
    path('save_case/', testcase_views.save_case),
    path('search_case_name/', testcase_views.search_case_name),
    path('del_case/<int:cid>/', testcase_views.del_case),
    path('update_case/', testcase_views.update_case),
    path('api_assert/', testcase_views.api_assert),


# 用例管理 -- 由JS调用的接口
    path("get_case_info/", testcase_api.get_case_info),
    path('get_porject_list/', testcase_api.get_porject_list),

]
