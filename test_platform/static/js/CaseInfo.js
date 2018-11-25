var CaseInfo = function (case_id) {
    
    function getCaseInfo() {
        $.post("/interface/get_case_info/", {
            "caseId": case_id,
        }, function (resp) {
            if (resp.success === "true"){
                let result = resp.data;
                document.getElementById("req_name").value = result.name;
                document.getElementById("req_url").value = result.url;
                document.getElementById("req_header").value = result.reqHeader;
                document.getElementById("req_parameter").value = result.reqParameter;
                // document.getElementById("assert_text").value = result.assertText;

                if(result.reqMethod === "post"){
                    document.getElementById("post").setAttribute("checked", "")
                }

                if (result.reqType === "json"){
                    document.getElementById("json").setAttribute("checked", "")
                }

                ProjectInit('project_name', 'module_name', result.projectName, result.moduleName);
            }

            else
            {
                 window.alert(resp.message);
            }
            
        });
        
    }
    getCaseInfo()
}