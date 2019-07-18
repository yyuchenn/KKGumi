function load_editor(qid) {
        $('#summernote').summernote({
        lang: 'zh-CN',
        airMode: false,
        placeholder: '点按这里开始键入内容',
        fontNames: ['Arial', 'Arial Black', 'Comic Sans MS', 'Courier New']
    });
    $(document).ready(function () {
        fetch("/resource/quest/" + qid + "/article.html").then(function(response) {
            if (response.status === 404)
                return  "";
            if (response.status === 403)
                return  "您暂无权限浏览。";
            return response.text();
        }).then(function (r) {
            console.log(r);
            $('#summernote').summernote("code", r);
        });
    });
}

function update_article(qid) {
    var article = $('#summernote').summernote('code');
    var postData = new FormData();
    postData.append("qid", qid);
    postData.append("article", article);
    fetch("/guild/update_article", {
        method: "POST",
        body: postData
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                console.log("success");
                break;
            case 1:
                return false;
            case 2:
                return false;
        }
    });
    return false;
}
