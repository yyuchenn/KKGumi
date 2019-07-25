function issue_icode() {
            var postData = new FormData();
            fetch(window.location.search,{
                method: "POST",
                body: postData,
                credentials: "same-origin"
            }).then(response => response.json()).then(function (j){
                //console.log(j.toString());
                switch (j["code"]) {
                    case 0:
                        window.location.href = window.location.href = '/dashboard/icode';
                        break;
                    case 1:
                        window.location.href = window.location.href = '/dashboard';
                        break;
                    case 2: break;
                }
            });
            return false;
        }
