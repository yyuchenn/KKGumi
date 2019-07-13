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


  return (dys !== 0?(dys+'天'):"") + (hrs !== 0?(hrs+'小时'):"") + (mins !== 0?(mins+'分钟'):"") + secs+'秒';
}

function localtime(stamp) {
    //TODO
}