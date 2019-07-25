function signup(user, pwd, pwd2) {
            user = user.value;
            pwd = pwd.value;
            pwd2 = pwd2.value;
            if (pwd !== pwd2) {
                $("#errorMessage").html("两次输入的密码不一致");
                        $("#errorArea").hide();
                        $("#errorMessage").show();
                        setTimeout(function () {
                            $("#errorArea").show();
                            $("#errorMessage").hide();
                        }, 1500);
                        return false;
            }
            var postData = new FormData();
            postData.append("user", user);
            postData.append("pwd", pwd);
            fetch(window.location.search,{
                method: "POST",
                body: postData,
                credentials: "same-origin"
            }).then(response => response.json()).then(function (j){
                switch (j["code"]) {
                    case 0:
                        try {
                            window.location.href = window.location.search.split("callback=")[1].split("&")[0];
                        }catch(e) {
                            window.location.href = "/dashboard";
                        } break;
                    case 1:
                        $("#errorMessage").html("邀请码错误或已过期");
                        $("#errorArea").hide();
                        $("#errorMessage").show();
                        setTimeout(function () {
                            $("#errorArea").show();
                            $("#errorMessage").hide();
                        }, 1500);
                        return false;
                    case 2:
                        $("#errorMessage").html("用户名已被占用");
                        $("#errorArea").hide();
                        $("#errorMessage").show();
                        setTimeout(function () {
                            $("#errorArea").show();
                            $("#errorMessage").hide();
                        }, 1500);
                        return false;
                    case 3:
                        $("#errorMessage").html("本站暂不开放注册");
                        $("#errorArea").hide();
                        $("#errorMessage").show();
                        setTimeout(function () {
                            $("#errorArea").show();
                            $("#errorMessage").hide();
                        }, 1500);
                        return false;
                    case 500:
                        $("#errorMessage").html("用户名或密码违规。密码为6-32位，可包含数字，字母，空格，或特殊字符(_@*.#!?-)。");
                        $("#errorArea").hide();
                        $("#errorMessage").show();
                        setTimeout(function () {
                            $("#errorArea").show();
                            $("#errorMessage").hide();
                        }, 5000);
                        return false;
                }
            });
            return false;
        }
