function export_word(qid, filename) {
    fetch("/resource/.sys/quest/" + qid + "/article.html").then(function (response) {
                if (response.status === 404)
                    console.log("");
                if (response.status === 403)
                    console.log("您暂无权限导出。");
                return response.text();
            }).then(function (r) {
                var docx = htmlDocx.asBlob(r);
                saveAs(docx, filename+".docx");
            });
    return false;
}

function export_txt(qid, filename) {
    fetch("/resource/.sys/quest/" + qid + "/article.html").then(function (response) {
                if (response.status === 404)
                    console.log("");
                if (response.status === 403)
                    console.log("您暂无权限导出。");
                return response.text();
            }).then(function (r) {
                var raw_text = r;
                raw_text = raw_text.replace(/<img .*?alt=["']?([^"']*)["']?.*?\/?>/g, "$1"); /* Use image alt text. */
                raw_text = raw_text.replace(/<a .*?href=["']?([^"']*)["']?.*?>(.*)<\/a>/g, "$2 [$1]"); /* Convert links to something useful */
                raw_text = raw_text.replace(/<(\/p|\/div|\/h\d|br)\w?\/?>/g,"\r\n"); /* Keep vertical whitespace intact. */
                raw_text = raw_text.replace(/<[A-Za-z/][^<>]*>/g, ""); /* Remove the rest of the tags. */
                var txt = new Blob([raw_text], {type:"text/plain"});
                saveAs(txt, filename+".txt");
            });
    return false;
}