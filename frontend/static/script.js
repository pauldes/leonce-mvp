function upvote(video_id) {
    let data = {}
    let url =  "/api/upvote/" + video_id;
    postRequest(data, url);
  }
  
function postRequest(data, url){ 
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () { 
        if (xhr.readyState === 4 && xhr.status != 200) {
            alert(this.responseText); 
        }
        else {
            console.log(this.responseText)
        }
    };
    var data = JSON.stringify(data);
    xhr.send(data); 
} 