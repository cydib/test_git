var TaskInfo = function (tid) {

    function getTaskInfo() {
        $.get("/interface/get_task_info/", {
            "taskId": tid,
        }, function (resp) {
            if (resp.success === "true"){
                let result = resp.data;
                document.getElementById("task_name").value = result.name;
                document.getElementById("task_des").value = result.url;
            }

            else
            {
                 window.alert(resp.message);
            }

        });

    }
    getTaskInfo()
}