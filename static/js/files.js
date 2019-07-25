function render_uploader(folder) {
    try {
        var uploader = new Dropzone("#dropzone", {
            url: '/upload_file',
            params: {
                folder: folder,
            }
        });
        uploader.on("success", function (file, response) {
            url = eval('(' + response + ')')['url'];
            filename = file.name;
            $("#pan_display").append(`<li class="list-group-item d-flex justify-content-between lh-condensed"><div><a class="my-0 h6" href="${url}">${filename}</a><br></div><div align="right"><div class="text-muted">刚刚</div>
                                        <button type="button" class="btn-sm btn-secondary disabled" disabled>删除</button></div></li>`
            )
        });
        return false;
    } catch (e) {
    }
}

function delete_file(uri, rid) {
    var postData = new FormData();
    postData.append('uri', uri);
    fetch("/delete_file", {
        method: "POST",
        body: postData,
        credentials: "same-origin"
    }).then(response => response.json()).then(function (j) {
        //console.log(j.toString());
        switch (j["code"]) {
            case 0:
                $(`#delete${rid}`).modal('hide');
                $(`#res${rid}`).attr('disabled','');
                $(`#res${rid}`).attr('class', 'btn btn-sm btn-secondary');
                $(`#res${rid}`).html('已删除');
                break;
            case 1:
                return false;
            case 2:
                return false;
        }
    });
    return false;
}

function new_folder(folder, dir_name) {
    dir_name = dir_name.value;
    var postData = new FormData();
    postData.append('folder', folder);
    postData.append('dir_name', dir_name);
    fetch("/new_dir", {
        method: "POST",
        body: postData,
        credentials: "same-origin"
    }).then(response => response.json()).then(function (j) {
        switch (j["code"]) {
            case 0:
                window.location.reload();
                break;
            case 1:
                return false;
            case 2:
                return false;
        }
    });
    return false;
}