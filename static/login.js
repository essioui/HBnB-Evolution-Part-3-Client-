document.addEventListener('DOMContentLoaded', () => {

    const token = getCookie('token');

    const loginLink = document.getElementById('login-link');

    if (token) {
        // hidden login if have token
        loginLink.style.display = 'none';
    } else {
        // if not have token affiche login
        loginLink.style.display = 'block';
    }
});




document.getElementById('login-form').addEventListener('submit', async function(event) {

    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {

        method: 'POST',
        headers: {

            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
    });

    if (response.ok) {

        const data = await response.json();

        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = '/';

    } else {

        const errorText = await response.json();

        document.getElementById('errorMessage').innerText = errorText.msg;
        
        // after message error affiche link of login for inscript
        document.getElementById('login-link').style.display = 'block';
    }
});




// read cookie by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}
