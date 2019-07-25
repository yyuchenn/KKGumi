function accept_quest(accept_uid, qid) {
    var postData = new FormData();
    postData.append("accept_uid", accept_uid);
    postData.append("qid", qid);
    fetch("/guild/accept_quest",{
                method: "POST",
                body: postData,
                credentials: "same-origin"
            }).then(response => response.json()).then(function (j){
                switch (j["code"]) {
                    case 0:
                        window.location.href = "/quest/" + qid;
                        break;
                    case 1:
                        document.getElementById("errorMessage").setAttribute("style", "color: #bd2130");
                        document.getElementById("errorMessage").innerHTML = "代理人无权限。";
                        return false;
                    case 2:
                        document.getElementById("errorMessage").setAttribute("style", "color: #bd2130");
                        document.getElementById("errorMessage").innerHTML = "承接人无权限。";
                        return false;
                    case 500:
                        document.getElementById("errorMessage").setAttribute("style", "color: #bd2130");
                        document.getElementById("errorMessage").innerHTML = "系统错误。";
                        return false;
                }
            });
            return false;
}