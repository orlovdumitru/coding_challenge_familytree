(function() {
    let all_rows = [];
    //get all everyone
    let xhr = new XMLHttpRequest();
    xhr.open(
        'GET',
        'get_all/' //'{% url "get_all/" %}'
    );
    xhr.onload = function() {
        if (xhr.status === 200) {
            let all_data = JSON.parse(xhr.responseText);
            let persons_table = document.querySelector('#main-table tbody');
            persons_table.innerHTML = '';
            let row = '';
            for (let person of all_data) {
                row += `
                    <tr attrid="person-${person['id']}">
                        <td>${person['first_name']} ${person['last_name']}</td>
                        <td>${person['phone_number']}</td>
                        <td>${person['email']}</td>
                        <td>${person['address']}</td>
                        <td>${person['birth_date']}</td>
                    </tr>
                `;
            }
            persons_table.innerHTML = row;
            addListenerToRows();
        } else {
            alert('Request failed.  Returned status of ' + xhr.status);
        }
    };
    xhr.send();

    function addListenerToRows() {
        all_rows = document.querySelectorAll('#main-table tbody tr');
        for (let row of all_rows) {
            // row.removeEventListener('click', getPersonInfo);
            row.addEventListener('click', getPersonInfo, false);
            row.param = this;
        }
        
        function getPersonInfo(row) {
            let element = row.currentTarget.getAttribute('attrid');
            let person_id = getId(element);
            let xhr = new XMLHttpRequest();
            window.location = `person/${person_id}`
            // xhr.open(
            //     'GET',
            //     'get_person/' + person_id
            // );
            // xhr.onload = function() {
            //     if (xhr.status === 200) {
            //         let person_info = JSON.parse(xhr.responseText);
            //         console.log(xhr.responseText)
            //         console.log(person_info)
            //         document.querySelector('first_name').value = person_info['first_name'];
            //         document.querySelector('last_name').value = person_info['last_name'];
            //         document.querySelector('phone_nr').value = person_info['phone_number'];
            //         document.querySelector('email').value = person_info['email'];
            //         document.querySelector('address').value = person_info['address'];
            //         document.querySelector('date_birth').value = person_info['date_birth'];

            //     } else {
            //         alert('Request failed.  Returned status of ' + xhr.status);
            //     }
            // };
            // xhr.send();

        }
    }

    function getId(id) {
        return id.split('-')[1];
    }

})();