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
            if (data.status === 'ok') {
                const friendButton = document.querySelector('button[type="submit"]');
                if (data.action === 'added') {
                    friendButton.textContent = 'Remove Friend';
                    friendButton.form.querySelector('input[name="action"]').value = 'remove';
                } else if (data.action === 'removed') {
                    friendButton.textContent = 'Add Friend';
                    friendButton.form.querySelector('input[name="action"]').value = 'add';
                }
            } else {
                console.error('Error adding/removing friend:', data.message);
            }
        })
        .catch
