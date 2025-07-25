document.addEventListener('DOMContentLoaded', function() {
    var loginForm = document.getElementById('loginForm');
    if (loginForm) {
        var usernameInput = loginForm.querySelector('input[name="username"]');
        var passwordInput = loginForm.querySelector('input[name="password"]');
        if (usernameInput) usernameInput.value = 'admin';
        if (passwordInput) passwordInput.value = 'intake';
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission
            var username = usernameInput.value;
            var password = passwordInput.value;
            var validUsername = 'admin';
            var validPassword = 'intake';
            if (username === validUsername && password === validPassword) {
                window.location.href = 'questionnaire.html';
            } else {
                alert('Invalid User ID or Password. Please try again.');
            }
        });
    }
});