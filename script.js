document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault(); // Prevent default form submission

            const username = loginForm.username.value;
            const password = loginForm.password.value;

            // --- IMPORTANT: This is for demonstration ONLY ---
            // In a real application, you would send these credentials to a server
            // for authentication. This client-side check is NOT secure.
            if (username === 'testuser' && password === 'testpass') {
                alert('Login successful! Redirecting to questionnaire...');
                window.location.href = 'questionnaire.html'; // Redirect to the questionnaire page
            } else {
                alert('Invalid User ID or Password. Please try again.');
            }
        });
    }
});