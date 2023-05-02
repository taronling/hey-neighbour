document.getElementById('add-friend-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const url = event.target.action;

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Friend added successfully, update the UI as needed
                console.log(data.message);
            } else {
                // Error occurred
                console.error(data.message);
            }
        })
        .catch(error => {
            console.error('Error adding friend:', error);
        });
});
