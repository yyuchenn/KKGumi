function create_manga(title, cover) {
            title = title.value;
            cover = cover.files[0];
            console.log(cover);
            var reader = new FileReader();
            reader.readAsDataURL(cover);
            reader.onloadend = function () {
                var c = this.result;
                console.log(c);
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
