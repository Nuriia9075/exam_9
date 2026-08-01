function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;}}}
    return cookieValue;
}
async function makeRequest(url, method = "POST") {
    let csrftoken= getCookie('csrftoken');
    let response = await fetch(url, { method: method,
        headers: {
        'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
    }
   });
    if (response.ok) {
        return await response.json();
    } else {
        return null;
    }
}
async function onFavorite(event) {
    event.preventDefault();
    let currentBtn = event.currentTarget;
    let url = currentBtn.dataset.url;
    let response = await makeRequest(url, "POST");
    if (response && response.status === 'ok') {
        let cardBody = currentBtn.closest('.favorite-container');
        if (cardBody) {
            let addBtn = cardBody.querySelector('.fav-btn-add');
            let removeBtn = cardBody.querySelector('.fav-btn-remove');
            if (response.is_favorite) {
                addBtn.classList.add('d-none');
                removeBtn.classList.remove('d-none');
            } else {
                removeBtn.classList.add('d-none');
                addBtn.classList.remove('d-none');
            }
        }
    } else {
        console.error("Ошибка ответ API");
    }
}

function onFavoriteLoad() {
    let favoriteButtons = document.querySelectorAll('[data-key="favorite"]');
    for (let btn of favoriteButtons) {
        btn.addEventListener('click', onFavorite);
    }
}
window.addEventListener("DOMContentLoaded", onFavoriteLoad);