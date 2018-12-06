var ProjectInit = function (_cmbProject, _cmbModule, defaultProject, defaultModule) {
    var cmbProject = document.getElementById(_cmbProject);
    var cmbModule = document.getElementById(_cmbModule);
    var dataList = [];


    //设置默认选项
    function cmbSelect(cmb, str) {
        for (var i = 0; i < cmb.options.length; i++) {
            if (cmb.options[i].value == str) {
                cmb.selectedIndex = i;
                return;
            }
        }
    }

    //创建下拉选项
    function cmbAddOption(cmb, str, obj) {
        var option = document.createElement("option");
        cmb.options.add(option);
        option.innerHTML = str;
        option.value = str;
        option.obj = obj;
    }

    //改变项目
    function changeProject() {
        cmbModule.options.length = 0;
        //cmbModule.onchange = null;
        if (cmbProject.selectedIndex == -1) {
            return;
        }
        var item = cmbProject.options[cmbProject.selectedIndex].obj;
        for (var i = 0; i < item.moduleList.length; i++) {
            cmbAddOption(cmbModule, item.moduleList[i], null);
        }
    }

    function getProjectList() {
        // 调用项目列表接口
        $.get("/interface/get_porject_list", {}, function (resp) {
            if (resp.success === "true") {
                dataList = resp.data;
                for (var i = 0; i < dataList.length; i++) {
                    cmbAddOption(cmbProject, dataList[i].name, dataList[i]);
                }

                cmbSelect(cmbProject, defaultProject);
                changeProject();
                cmbProject.onchange = changeProject;
            }

            cmbSelect(cmbProject, defaultProject);
        });
    }

    // 调用getProjectList函数
    getProjectList();

};


// 获取用例列表

var CaseListInit = function () {

    var options = "";

    function getCaseListInfo() {
        $.get("/interface/get_case_list", {}, function (resp) {
            if (resp.success === "true") {
                // console.log(resp.data);
                let cases = resp.data;

                for (let i = 0; i < cases.length; i++) {
                    let option = '<input type="checkbox" name="ids" value="' + cases[i].id + '" /> ' + cases[i].name + '<br>'
                    options += option;
                }

                let devCaseList = document.querySelector(".caseList");
                let sall = '<input type="checkbox" id="selectAll"/>全选 / 取消<br>'
                let all = sall + options;
                devCaseList.innerHTML = all;
            }
            else {
                alert(resp.message);
            }

            $("#selectAll").click(function() {
            $(":checkbox[name='ids']").prop("checked", this.checked);
        });

        });

    }

    getCaseListInfo();
};