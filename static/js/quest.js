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
                return false;
        }
    });
    return false;
}