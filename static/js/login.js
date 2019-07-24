function login(user, pwd) {
            user = user.value;
            pwd = pwd.value;
            var postData = new FormData();
            postData.append("user", user);
            postData.append("pwd", pwd);
            fetch(window.location.search,{
                method: "POST",
                body: postData
            }).then(response => response.json()).then(function (j){
                //console.log(j.toString());
                switch (j["code"]) {
                    case 0:
                        try {
                            window.location.href = window.location.search.split("callback=")[1].split("&")[0];
                        }catch(e) {
                            window.location.href = "/dashboard";
                        } break;
                    case 1:
                        $("#errorMessage").html("用户名或密码不正确");
                        $("#errorArea").hide();
                        $("#errorMessage").show();
                        setTimeout(function () {
                            $("#errorArea").show();
                            $("#errorMessage").hide();
                        }, 1500);
                        return false;
                    case 2:
                        document.getElementById("errorMessage").setAttribute("style", "color: #bd2130");
                        return false;
                    case 500:
                        $("#errorMessage").html("用户名或密码不合法");
                        $("#errorArea").hide();
                        $("#errorMessage").show();
                        setTimeout(function () {
                            $("#errorArea").show();
                            $("#errorMessage").hide();
                        }, 1500);
                        return false;
                }
            });
            return false;
        }
