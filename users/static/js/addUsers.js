document.getElementById('add-friend-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const url = event.target.getAttribute('action');

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                if (data.action === 'added') {
                    event.target.querySelector('button').textContent = 'Remove Friend';
                    event.target.querySelector('input[name="action"]').value = 'remove';
                } else if (data.action === 'removed') {
                    event.target.querySelector('button').textContent = 'Add Friend';
                    event.target.querySelector('input[name="action"]').value = 'add';
                }
            } else {
                console.error('Error adding/removing friend:', data.message);
            }
        })
        .catch(error => {
            console.error('Error adding/removing friend:', error);
        });
});
