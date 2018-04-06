function updateTime() {
    let timeTab = document.getElementsByClassName('time');
    let timestampTab = document.getElementsByClassName('timestamp');
    let tabResult = document.getElementsByClassName("result");
    let n2 = Date.now();
    for (let i = 0; i < timeTab.length; i++) {
        let delta = timestampTab[i].innerHTML - n2 / 1000;
        if (delta <= 0) {
            timeTab[i].innerHTML = 'Finished';
            tabResult[i].style.display = "block";
        }
        else {
            delta = Math.ceil(delta);
            let hour = Math.floor(delta / 3600);
            delta -= 3600 * hour;
            let minute = Math.floor(delta / 60);
            delta -= 60 * minute;
            timeTab[i].innerHTML = hour + ":" + minute + ":" + delta;
        }
    }
}

updateTime();
setInterval(updateTime, 1000);
