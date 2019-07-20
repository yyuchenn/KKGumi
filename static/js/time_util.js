function timelapse(stamp) {
    var create_time = new Date(stamp * 1000);
    var current_time = new Date().getTime();
    var lapse =  current_time - create_time;
    return ms2string(lapse);
}

function ms2string(s) {
  var ms = s % 1000;
  s = (s - ms) / 1000;
  var secs = s % 60;
  s = (s - secs) / 60;
  var mins = s % 60;
  s = (s - mins) / 60;
  var hrs = s % 24;
  var dys = (s - hrs) / 24;



  return (dys !== 0?(dys+'天'):"") + (hrs !== 0 || dys !== 0?(("0"+hrs).slice(-2)+'小时'):"") + (mins !== 0 || hrs !== 0 || dys !== 0 ?(("0"+mins).slice(-2)+'分钟'):"") + ("0"+secs).slice(-2) +'秒';
}

function setTimer(id, stamp) {
    // jQuery Required
    $().ready(function () {
        $("#" + id).html(timelapse(stamp));
    });
    setInterval(function () {
        $("#" + id).html(timelapse(stamp));
    }, 1000);
}

function setLocalTime(id, stamp) {
    $().ready(function () {
        $("#" + id).html(localtime(stamp));
    });
}

function setLocalTime_exact(id, stamp) {
    $().ready(function () {
        $("#" + id).html(localtime_exact(stamp));
    });
}

function localtime(stamp) {
    var time = new Date(stamp * 1000);
    return time.getFullYear() + "年" + (time.getMonth()+1) + "月" + time.getDate() + "日";
}

function localtime_exact(stamp) {
    var time = new Date(stamp * 1000);
    return time.getFullYear() + "年" + (time.getMonth()+1) + "月" + time.getDate() + "日 " + ("0"+time.getHours()).slice(-2) + ":" + ("0"+time.getMinutes()).slice(-2);
}