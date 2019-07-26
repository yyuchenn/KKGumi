function load_editor(qid, proof_mode=false) {
    $('#summernote').summernote({
        lang: 'zh-CN',
        airMode: false,
        toolbar: [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
        placeholder: '点按这里开始键入内容',
        fontNames: ['方正新书宋', '方正兰亭刊黑', 'Courier New'],
        fontNamesIgnoreCheck: ['方正新书宋', '方正兰亭刊黑'],
        callbacks: {
            onImageUpload: function (files, editor, $editable) {
                UploadFiles(files, insertImg, qid);
            },
            onMediaDelete: function (target) {
            },
            onInit: function () {
                unchange();
            },
            onChange: proof_mode? function () {
                change();
                article = $('#summernote').summernote("code");
                $("#comparing_area").html(htmldiff(original, article));
            }: function () {
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
        credentials: "same-origin"
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
        body: postData,
        credentials: "same-origin"
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