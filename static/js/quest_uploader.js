function load_editor(qid) {
    $('#summernote').summernote({
        lang: 'zh-CN',
        airMode: false,
        placeholder: '点按这里开始键入内容',
        fontNames: ['Arial', 'Arial Black', 'Comic Sans MS', 'Courier New'],
        callbacks: {
            onImageUpload: function (files, editor, $editable) {
                UploadFiles(files, insertImg, qid);
            },
            onMediaDelete: function (target) {
            },
            onInit: function () {
                unchange();
            },
            onChange: function () {
                change();
            }
        }
    });
}


function insertImg(urls) {
    for (tag in urls) {
        $('#summernote').summernote('editor.insertImage', urls[tag], function ($image) {
            $image.css({
                display: '',
                width: '100%'
            })
        });
    }
}


function UploadFiles(files, func, qid) {
    var formData = new FormData();
    formData.append('qid', qid);
    for (f in files) {
        formData.append(f, files[f]);
    }

    fetch("/guild/upload_file", {
        method: "POST",
        body: formData,
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                urls = j["urls"];
                func(urls);
                break;
            case 500:
                return false;
        }
    });
    return false;
}

function update_article(qid) {
    var article = $('#summernote').summernote('code');
    var postData = new FormData();
    postData.append("qid", qid);
    postData.append("article", article);
    fetch("/guild/update_article", {
        method: "POST",
        body: postData
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                saved();
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