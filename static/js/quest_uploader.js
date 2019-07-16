$(document).ready(function () {
                $('#summernote').summernote({
                    lang: 'zh-CN',
                    airMode: false,
                    placeholder: '点按这里开始键入内容',
                    fontNames: ['Arial', 'Arial Black', 'Comic Sans MS', 'Courier New']
                });
            });
function update_article(qid) {
            var article = $('#summernote').summernote('code');
            var postData = new FormData();
            postData.append("qid", qid);
            postData.append("article", article);
            fetch("/guild/update_article",{
                method: "POST",
                body: postData
            }).then(response => response.json()).then(function (j){
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
