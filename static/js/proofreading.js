function fetch_original(my_qid, target_qid, to_article=false) {
    target_qid = target_qid.value;
    to_article = to_article.checked;
    postData = new FormData();
    postData.append("my_qid", my_qid);
    postData.append("target_qid", target_qid);
    postData.append("to_article", to_article);
    fetch('/guild/fetch_original', {
        method: "POST",
        body: postData,
        credentials: "same-origin"
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                window.location.reload();
                break;
            case 1:
                console.log("");
                return false;
        }
    });
    return false;
}

function trigger_fetch_modal() {
    if (isChanged) {
        $("#unsave_fetch_confirm").modal("show");
    }else {
        $("#fetch_form").modal("show");
    }
    return false;
}