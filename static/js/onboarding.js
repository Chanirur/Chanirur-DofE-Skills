const URL = '/onboarding'

let button = document.querySelector('#submitDetails');
button.addEventListener('click', function () {
    let firstname = document.querySelector('#firstname').value;
    let surname = document.querySelector('#surname').value;
    if (firstname && surname) {
        let detailsData = {
            method: 'POST',
            headers: {
                'content-type': 'application/json',
            },
            body: JSON.stringify({
                'name': 'details',
                'firstname': firstname,
                'surname': surname
            })
        }
        fetch(URL, detailsData)
            .then(response => response.json())
            .catch(error => console.error('Error:', error))
    }
})

