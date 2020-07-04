$(document).ready(function(){
    var myDiv = document.getElementById("likes_count");
            
    var since = 0;
    setInterval(function(){ 
        since = since + 1
        myDiv.innerHTML = since;
    }, 3000);
});