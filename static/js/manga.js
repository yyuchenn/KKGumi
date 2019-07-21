function create_manga(title, cover) {
    title = title.value;
    cover = cover.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(cover);
    reader.onloadend = function () {
        var c = this.result;
        var postData = new FormData();
        postData.append("title", title);
        postData.append("cover", c);
        fetch("/admin/add_manga", {
            method: "POST",
            body: postData
        }).then(response => response.json()).then(function (j) {
            //console.log(j.toString());
            switch (j["code"]) {
                case 0:
                    window.location.reload();
                    break;
                case 1:
                    document.getElementsByClassName("errorMessage").setAttribute("style", "color: #bd2130");
                    document.getElementsByClassName("errorMessage").innerHTML = "上传失败";
                    return false;
            }
        });
    };
    return false;
}


function create_chapter(title, mid) {
    title = title.value;
    postData = new FormData();
    postData.append("title", title);
    postData.append("mid", mid);
    fetch("/admin/add_chapter", {
        method: "POST",
        body: postData
    }).then(response => response.json()).then(function (j) {
        //console.log(j.toString());
        switch (j["code"]) {
            case 0:
                window.location.reload();
                break;
            case 1:
                document.getElementsByClassName("errorMessage").setAttribute("style", "color: #bd2130");
                document.getElementsByClassName("errorMessage").innerHTML = "权限不足。";
                return false;
            case 2:
                document.getElementsByClassName("errorMessage").setAttribute("style", "color: #bd2130");
                document.getElementsByClassName("errorMessage").innerHTML = "漫画不存在。";
                return false;
        }
    });
    return false;
}


function create_quest(name, type, accessibility, cid) {
    name = name.value;
    type = type.value;
    accessibility = accessibility.value;
    postData = new FormData();
    postData.append("name", name);
    postData.append("quest_type", type);
    postData.append("public_accessibility", accessibility);
    postData.append("cid", cid);
    fetch("/admin/add_quest", {
        method: "POST",
        body: postData
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                window.location.reload();
                break;
            case 1:
                document.getElementsByClassName("errorMessage2").setAttribute("style", "color: #bd2130");
                document.getElementsByClassName("errorMessage2").innerHTML = "权限不足。";
                return false;
            case 2:
                document.getElementsByClassName("errorMessage").setAttribute("style", "color: #bd2130");
                document.getElementsByClassName("errorMessage").innerHTML = "章节不存在。";
                return false;
        }
    });
    return false;
}


function change_manga_title(new_title, mid) {
    new_title = new_title.value;
    postData = new FormData();
    postData.append("new_title", new_title);
    postData.append("mid", mid);
    fetch("/admin/change_manga_title", {
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
}


function change_manga_cover(cover, mid) {
    cover = cover.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(cover);
    reader.onloadend = function () {
        var c = this.result;
        var postData = new FormData();
        postData.append("new_cover", c);
        postData.append("mid", mid);
        fetch("/admin/change_manga_cover", {
            method: "POST",
            body: postData
        }).then(response => response.json()).then(function (j) {
            //console.log(j.toString());
            switch (j["code"]) {
                case 0:
                    window.location.reload();
                    break;
                case 1:
                    document.getElementsByClassName("errorMessage").setAttribute("style", "color: #bd2130");
                    document.getElementsByClassName("errorMessage").innerHTML = "上传失败";
                    return false;
            }
        });
    };
    return false;
}

function change_manga_status(new_title, mid) {
    new_title = new_title.value;
    postData = new FormData();
    postData.append("new_status", new_title);
    postData.append("mid", mid);
    fetch("/admin/change_manga_status", {
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
                console.log("错误的漫画编码。");
                return false;
        }
    });
}

function chapter_mark(cid, mark) {
    postData = new FormData();
    postData.append("cid", cid);
    postData.append("mark", mark);
    fetch('/admin/chapter_mark', {
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


function load_editor() {
    $('.summernote').summernote({
        lang: 'zh-CN',
        airMode: true,
        placeholder: '点按这里开始键入内容',
        fontNames: ['Arial', 'Arial Black', 'Comic Sans MS', 'Courier New'],
    });
    $('#editor_edit').attr('style', 'display: none;');
    $('#editor_cancel').attr('style', '');
    $('#editor_save').attr('style', '');
    return false;
}

function destry_editor() {
    $('.summernote').summernote('destroy');
    $('#editor_edit').attr('style', '');
    $('#editor_cancel').attr('style', 'display: none;');
    $('#editor_save').attr('style', 'display: none;');
    return false;
}

function save_notes(mid) {
    postData = new FormData();
    var notes = $('.summernote').summernote('code');
    postData.append("notes", notes);
    postData.append("mid", mid);
    fetch("/guild/change_notes", {
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
                console.log("错误的漫画编码。");
                return false;
        }
    });
    destry_editor();
    return false;
}

function delete_chapter(cid) {
    var postData = new FormData();
    postData.append("cid", cid);
    fetch("/admin/delete_chapter", {
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


function delete_manga(mid) {
    // 已弃用
    var postData = new FormData();
    postData.append("mid", mid);
    fetch("/admin/delete_manga", {
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