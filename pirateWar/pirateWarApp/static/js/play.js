function updateTime() {
    var timeTab = document.getElementsByClassName('time');
    var timestampTab = document.getElementsByClassName('timestamp');
    var tabResult = document.getElementsByClassName("result");
    var n2 = Date.now();
    for (var i = 0; i < timeTab.length; i++) {
        delta = timestampTab[i].innerHTML - n2 / 1000;
        if (delta <= 0) {
            timeTab[i].innerHTML = 'Finished';
            tabResult[i].style.display = "block";
        }
        else {
            if(!img.classList.contains("ship_animate"))
            {
                img.classList.add("ship_animate");
                img.classList.remove("ship");
            }

            delta = Math.ceil(delta);
            var hour = Math.floor(delta / 3600);
            delta -= 3600 * hour;
            var minute = Math.floor(delta / 60);
            delta -= 60 * minute;
            timeTab[i].innerHTML = hour + ":" + minute + ":" + delta;
        }
    }
}
function check_and_change_class(){
    if (delta <= 0 && img.classList.contains("ship_animate")) {
        img.classList.remove("ship_animate");
        img.classList.add("ship");
    }
}
var delta = 0;
var img = document.getElementById("ship");
img.addEventListener("animationiteration", check_and_change_class, false);
updateTime();
setInterval(updateTime, 1000);
