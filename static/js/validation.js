// static/js/validation.js

document.addEventListener('DOMContentLoaded', function() {
    
    // --- LÓGICA GENERAL DE VALIDACIÓN ---

    // Función para validar un campo de entrada específico (vacío)
    function validateField(inputElement) {
        const feedbackElement = document.getElementById(inputElement.id + '-feedback');
        const trimmedValue = inputElement.value.trim();
        let errorMessage = '';

        if (trimmedValue === '') {
            errorMessage = 'Este campo no puede estar vacío.';
        } 
        
        // Aplicar estilos y mensajes de error
        if (errorMessage) {
            inputElement.classList.add('is-invalid');
            inputElement.classList.remove('is-valid');
            if (feedbackElement) feedbackElement.textContent = errorMessage;
            return false;
        } else {
            inputElement.classList.remove('is-invalid');
            inputElement.classList.add('is-valid');
            if (feedbackElement) feedbackElement.textContent = '';
            return true;
        }
    }

    // --- MANEJO DEL FORMULARIO DE LOGIN ---
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');

        // Validar en tiempo real
        usernameInput.addEventListener('input', function() { validateField(this); });
        passwordInput.addEventListener('input', function() { validateField(this); });

        // Validar al enviar
        loginForm.addEventListener('submit', function(event) {
            const isUsernameValid = validateField(usernameInput);
            const isPasswordValid = validateField(passwordInput);

            if (!isUsernameValid || !isPasswordValid) {
                event.preventDefault(); 
            }
        });
    }

    // --- MANEJO DEL FORMULARIO DE REGISTRO ---
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirm_password');

        // Validar en tiempo real (Username y Passwords)
        usernameInput.addEventListener('input', function() { validateField(this); });
        passwordInput.addEventListener('input', function() { validateField(this); checkPasswordMatch(); });
        confirmPasswordInput.addEventListener('input', function() { validateField(this); checkPasswordMatch(); });

        // Función específica para verificar que las contraseñas coincidan
        function checkPasswordMatch() {
            const matchFeedback = document.getElementById('confirm_password-feedback');
            
            if (passwordInput.value !== confirmPasswordInput.value) {
                confirmPasswordInput.classList.add('is-invalid');
                confirmPasswordInput.classList.remove('is-valid');
                matchFeedback.textContent = 'Las contraseñas no coinciden.';
                return false;
            } else if (passwordInput.value.trim() !== '') {
                confirmPasswordInput.classList.remove('is-invalid');
                confirmPasswordInput.classList.add('is-valid');
                matchFeedback.textContent = '';
                return true;
            }
            return validateField(confirmPasswordInput);
        }

        // Validar al enviar
        registerForm.addEventListener('submit', function(event) {
            const isUsernameValid = validateField(usernameInput);
            const isPasswordValid = validateField(passwordInput);
            const isConfirmPasswordValid = validateField(confirmPasswordInput);
            const passwordsMatch = checkPasswordMatch();

            if (!isUsernameValid || !isPasswordValid || !isConfirmPasswordValid || !passwordsMatch) {
                event.preventDefault(); 
            }
        });
    }

});