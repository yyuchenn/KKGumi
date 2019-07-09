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


function create_quest(name, type, cid) {
    name = name.value;
    type = type.value;
    postData = new FormData();
    postData.append("name", name);
    postData.append("quest_type", type);
    postData.append("cid", cid);
    fetch("/admin/add_quest", {
        method: "POST",
        body: postData
    }).then(response => response.json()).then(function (j) {
        //console.log(j.toString());
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