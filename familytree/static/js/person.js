(function() {
   

})();

document.getElementById('create-relation-form').addEventListener('submit', function(event){
    event.preventDefault();
    var form = this;
    var data = new FormData(form);
    let xhr = new XMLHttpRequest();
    xhr.open(
        'POST',
        `/create_relation/`,
        false
    );
    // xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        if (xhr.status === 200 && xhr.responseText !== newName) {
            let created_relation = JSON.parse(xhr.responseText);
            console.log(created_relation)
            alert('Something went wrong.  Name is now ' + xhr.responseText);
        }
        else if (xhr.status !== 200) {
            alert('Request failed.  Returned status of ' + xhr.status);
        }
    };
    xhr.send(data);
});