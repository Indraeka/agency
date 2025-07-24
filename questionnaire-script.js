document.addEventListener('DOMContentLoaded', () => {
    const questionnaireForm = document.getElementById('questionnaireForm');

    if (questionnaireForm) {
        questionnaireForm.addEventListener('submit', (event) => {
            event.preventDefault(); // Prevent default form submission

            const formData = new FormData(questionnaireForm);
            let emailBody = "Questionnaire Responses:\n\n";

            // Iterate over all form fields
            for (let [name, value] of formData.entries()) {
                if (name === 'fruitsLiked') { // Special handling for multiple checkboxes
                    const checkedFruits = [];
                    questionnaireForm.querySelectorAll(`input[name="fruitsLiked"]:checked`).forEach(checkbox => {
                        checkedFruits.push(checkbox.value);
                    });
                    emailBody += `${name}: ${checkedFruits.join(', ')}\n`;
                } else {
                    emailBody += `${name}: ${value}\n`;
                }
            }

            const recipientEmail = 'your-email@example.com'; // **CHANGE THIS TO YOUR EMAIL ADDRESS**
            const emailSubject = 'Questionnaire Submission';
            const mailtoLink = `mailto:${recipientEmail}?subject=${encodeURIComponent(emailSubject)}&body=${encodeURIComponent(emailBody)}`;

            window.location.href = mailtoLink; // This will prompt the user's email client
            alert('Your email client will open with the questionnaire answers. Please click send.');
        });
    }
});