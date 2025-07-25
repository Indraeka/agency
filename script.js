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

    var registrationForm = document.getElementById('registrationForm');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(event) {
            event.preventDefault();
            var firstname = registrationForm.querySelector('input[name="firstname"]').value;
            var lastname = registrationForm.querySelector('input[name="lastname"]').value;
            var email = registrationForm.querySelector('input[name="email"]').value;
            // Generate random 7-digit code
            var confirmationCode = Math.floor(1000000 + Math.random() * 9000000).toString();
            // Store info in localStorage
            localStorage.setItem('registration_firstname', firstname);
            localStorage.setItem('registration_lastname', lastname);
            localStorage.setItem('registration_email', email);
            localStorage.setItem('confirmation_code', confirmationCode);
            // Show code to user
            alert('Your confirmation code is: ' + confirmationCode + '\nPlease remember this code. You will need it at the end of the intake questionnaire.');
            // Redirect to questionnaire
            window.location.href = 'questionnaire.html';
        });
    }
});
