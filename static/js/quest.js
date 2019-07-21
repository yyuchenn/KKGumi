function finish_quest(qid) {
    var postData = new FormData();
    postData.append("qid", qid);
    fetch("/guild/finish_quest", {
        method: "POST",
        body: postData
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                window.location.reload();
                break;
            case 1:
                return false;
        }
    });
    return false;
}

function transfer_quest(qid) {
    var postData = new FormData();
    postData.append("qid", qid);
    fetch("/guild/transfer_quest", {
        method: "POST",
        body: postData
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                window.location.reload();
                break;
            case 1:
                return false;
        }
    });
    return false;
}

function close_quest(qid) {
    var postData = new FormData();
    postData.append("qid", qid);
    fetch("/guild/close_quest", {
        method: "POST",
        body: postData
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                window.location.reload();
                break;
            case 1:
                return false;
        }
    });
    return false;
}

function reopen_quest(qid) {
    var postData = new FormData();
    postData.append("qid", qid);
    fetch("/guild/reopen_quest", {
        method: "POST",
        body: postData
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                window.location.reload();
                break;
            case 1:
                console.log("权限不足。");
                return false;
        }
    });
    return false;
}

function change_quest_accessibility(qid, new_accessibility) {
    var postData = new FormData();
    postData.append("qid", qid);
    postData.append("new_accessibility", new_accessibility);
    fetch("/admin/change_quest_accessibility", {
        method: "POST",
        body: postData
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                window.location.reload();
                break;
            case 1:
                console.log("权限不足。");
                return false;
            case 2:
                console.log("任务还未完成或停止。");
                return false;
        }
    });
    return false;
}

function delete_quest(qid, mid) {
        var postData = new FormData();
    postData.append("qid", qid);
    fetch("/admin/delete_quest", {
        method: "POST",
        body: postData
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                window.location.href = '/manga/'+mid;
                break;
            case 1:
                console.log("权限不足。");
                return false;
        }
    });
    return false;
}