(function() {

    // document.querySelector('#create-relation-btn').addEventListener('click', create_relation);

   
    

})();

function create_relation(rawForm, id){
    let elements = rawForm.form.elements;
    let params = '';
    let value;
    // let relation_form = document.querySelector('#create-relation-form');
    // relation_form = JSON.parse(relation_form);
    for (let i = 0; i < elements.length; i++){
        params += elements[i].name + "=" + encodeURIComponent(value) + "&";
    }
    // let formData = new FormData();
    // formData.append
    // console.log('works')
    // console.log(relation_form)
    let xhr = new XMLHttpRequest();
    xhr.open(
        'POST',
        "create_relation/"+id,
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
    xhr.send(params);
}