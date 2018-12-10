var TaskInfo = function (tid) {
    function getTaskInfo() {
        $.get("/interface/get_task_info/", {
            "taskId": tid,
        }, function (resp) {
            if (resp.success === "true") {
                let result = resp.data;
                document.getElementById("task_name").value = result.task_name;
                document.getElementById("task_des").value = result.task_des;
                let task_status = result.task_status;
                switch (task_status) {
                    case 0:
                        document.getElementById("notperformed").setAttribute("checked", "");
                        break;
                    case 1:
                        document.getElementById("performing").setAttribute("checked", "");
                        break;
                    case 2:
                        document.getElementById("performed").setAttribute("checked", "");
                        break;
                    case 3:
                        document.getElementById("waiting").setAttribute("checked", "");
                        break;
                }

                let test_case = result.task_case;
                var options = "";
                for(let i = 0 ; i< test_case.length; i++)
                {
                    let status = test_case[i].select===true?"checked":"";
                    let option = '<input type="checkbox" name="ids" value="'
                        + test_case[i].case_id
                        + '"'+status+'/>'
                        + test_case[i].case_name
                        + '<br>'
                    options += option;
                }

                let devCaseList = document.querySelector(".caseList");
                let sall = '<input type="checkbox" id="selectAll"/>全选 / 取消<br>'
                let all = sall + options;
                devCaseList.innerHTML = all;

                 $("#selectAll").click(function () {
                $(":checkbox[name='ids']").prop("checked", this.checked);
            });

            }

            else {
                window.alert(resp.message);
            }

        });

    }

    getTaskInfo()
}