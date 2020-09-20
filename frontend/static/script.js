function upvote(video_id) {
    let data = {}
    let url =  "/api/upvote/" + video_id;
    postRequest(data, url, video_id);
  }

function incrementVoteCount(video_id){
    var elem_id = "vote-total-number-" + video_id
    var vote_number = document.getElementById(elem_id).innerHTML;
    var new_vote_number = parseInt(vote_number) + 1
    document.getElementById(elem_id).innerHTML = new_vote_number;
}
  
function postRequest(data, url, video_id){
    var success = false
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () { 
        if (xhr.readyState === 4 && xhr.status != 200) {
            console.error(this.responseText);
        }
        else if (xhr.readyState === 4 && xhr.status === 200) {
            //console.log(this.responseText);
            incrementVoteCount(video_id);
        }
    };
    var data = JSON.stringify(data);
    xhr.send(data);
} 