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
                let task_case = result.task_case.split(",");
                // console.log(document.getElementsByName("ids"))
                console.log(document.getElementById("cases_1"))
                // for (let i = 0; i < task_case.length; i++) {
                //     console.log(i, task_case[i])
                //     console.log(cases[i].value)
                //     if (document.getElementsByName("ids")[i].value === result.task_case.split(",")[i]) {
                //         document.getElementsByName("ids")[i].checked = true;
                //     }
                // }
            }

            else {
                window.alert(resp.message);
            }

        });

    }

    getTaskInfo()
}