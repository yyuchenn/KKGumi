function is_success() {

}


function change_nickname(new_nickname) {
    new_nickname = new_nickname.value;
    var postData = new FormData();
    postData.append("new_nickname", new_nickname);
    fetch('/dashboard/change_nickname', {
        method: "POST",
        body: postData,
        credentials: "same-origin"
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                $('#success-pop').attr("style", "");
                $('.nickname').html(new_nickname);
                console.log(new_nickname.value);
                break;
            case 1:
                return false;
        }
    });
    return false;
}

function change_introduction(new_introduction) {
    new_introduction = new_introduction.value;
    var postData = new FormData();
    postData.append("new_introduction", new_introduction);
    fetch('/dashboard/change_introduction', {
        method: "POST",
        body: postData,
        credentials: "same-origin"
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                $('#success-pop').attr("style", "");
                break;
            case 1:
                return false;
        }
    });
    return false;
}

function change_password(old_password, new_password, new_password_repeat) {
    old_password = old_password.value;
    new_password = new_password.value;
    new_password_repeat = new_password_repeat.value;
    if (new_password !== new_password_repeat) {
        document.getElementById("errorMessage").setAttribute("style", "color: #bd2130");
        document.getElementById("errorMessage").innerHTML = "两次输入的密码不一致，请重试。";
        return false;
    }
    var postData = new FormData();
    postData.append("old_password", old_password);
    postData.append("new_password", new_password);
    fetch('/dashboard/change_password', {
        method: "POST",
        body: postData,
        credentials: "same-origin"
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                try {
                    window.location.href = window.location.search + "?success=1";
                } catch (e) {
                    window.location.href = "/dashboard";
                }
                break;
            case 1:
                document.getElementById("errorMessage").setAttribute("style", "color: #bd2130");
                document.getElementById("errorMessage").innerHTML = "旧密码错误。";
                return false;
            case 2:
                document.getElementById("errorMessage").setAttribute("style", "color: #bd2130");
                document.getElementById("errorMessage").innerHTML = "密码违规。密码为6-32位，可包含数字，字母，空格，或特殊字符(_@*.#!?-)。";
                return false;
            case 500:
                document.getElementById("errorMessage").setAttribute("style", "color: #bd2130");
                document.getElementById("errorMessage").innerHTML = "旧密码违规。";
                return false;
        }
    });
    return false;
}
