function render_uploader(folder) {
    try {
        var myDropzone = new Dropzone("#dropzone", {
            url: '/upload_file',
            params: {
                folder: folder,
            }
        });
        return false;
    } catch (e) {
    }
}

function delete_file(uri) {
    var postData = new FormData();
    postData.append('uri', uri);
    fetch("/delete_file", {
        method: "POST",
        body: postData
    }).then(response => response.json()).then(function (j) {
        //console.log(j.toString());
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