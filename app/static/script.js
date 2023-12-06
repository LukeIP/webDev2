$(document).on('click', '.like-button', function(e){
    e.preventDefault();
    // getting post id
    let like_id = e.target.id;
    $.getJSON('/like/'+like_id, function(data) {

    });
    setTimeout(function(){
        window.location.reload();
    },500);
})