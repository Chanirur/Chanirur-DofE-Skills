const dataToSend = {
    name: 'John Doe',
    age: 30
};

fetch('/ajax', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(dataToSend)
})
    .then(response => response.json())
    .then(data => {
        console.log('Response from backend:', data);
        alert('Response: ' + data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
