function displaySearchResults(users) {
    const searchResultsDiv = document.getElementById('search-results');
    searchResultsDiv.innerHTML = '';

    if (users.length === 0) {
        searchResultsDiv.innerHTML = '<p class="p-2 text-gray-500">No results found</p>';
        return;
    }

    users.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.classList.add('p-2', 'border-b', 'border-gray-200');

        // Create an anchor element for the user's profile link
        const userProfileLink = document.createElement('a');
        userProfileLink.href = `/user/profile/${user.pk}/`;
        userProfileLink.innerHTML = `<span class="font-semibold">${user.fields.username}</span> (${user.fields.first_name} ${user.fields.last_name})`;

        // Append the anchor element to the userDiv
        userDiv.appendChild(userProfileLink);

        searchResultsDiv.appendChild(userDiv);
    });
}


function searchUsers(query) {
    if (!query) {
        displaySearchResults([]);
        return;
    }

    const url = `/search_users/?query=${query}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const users = JSON.parse(data.users);
            displaySearchResults(users);
        })
        .catch(error => {
            console.error('Error fetching search results:', error);
        });
}

const searchInput = document.getElementById('topbar-search');

searchInput.addEventListener('input', (event) => {
    const query = event.target.value;
    searchUsers(query);
});
