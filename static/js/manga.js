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
                            document.getElementById("errorMessage").setAttribute("style", "color: #bd2130");
                            document.getElementById("errorMessage").innerHTML = "上传失败";
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
                        document.getElementById("errorMessage").setAttribute("style", "color: #bd2130");
                        document.getElementById("errorMessage").innerHTML = "权限不足。";
                        return false;
                    case 2:
                        document.getElementById("errorMessage").setAttribute("style", "color: #bd2130");
                        document.getElementById("errorMessage").innerHTML = "漫画不存在。";
                        return false;
                }
            });
            return false;
        }
