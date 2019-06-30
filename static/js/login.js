function smt(user,pwd) {
            user = user.value;
            pwd = pwd.value;
            var postData = new FormData();
            postData.append("user", user);
            postData.append("pwd", pwd);
            fetch("/login",{
                method: "POST",
                body: postData
            }).then(function (j){
                console.log(j);
                /*
                try {
                    window.location.href = window.location.search.split("callback=")[1].split("&")[0];
                }catch(e) {
                     window.location.href = "/";
                }*/

            });
            return false;
        }
