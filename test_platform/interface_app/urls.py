from django.urls import path
from interface_app.views import testcase_views

urlpatterns = [
    path('case_manage/', testcase_views.case_manage),
    path('add_case/', testcase_views.add_case),
    path('debug_case/', testcase_views.debug_case),
    path('edit_case/<int:cid>/', testcase_views.edit_case),
    path('get_porject_list/', testcase_views.get_porject_list),
    path('save_case/', testcase_views.save_case),
    path('search_case_name/', testcase_views.search_case_name)

]
