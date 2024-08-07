const themeToggle = document.getElementById('theme-toggle');
const logoImg = document.getElementById('logo-img');
const userOptionsMenu = document.getElementById('user-options');

function updateThemeToggleText() {
    if (document.body.classList.contains('dark-mode')) {
        themeToggle.innerHTML = '<i class="fas fa-sun"></i> Modo Claro';
    } else {
        themeToggle.innerHTML = '<i class="fas fa-moon"></i> Modo Oscuro';
    }
}

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    if (document.body.classList.contains('dark-mode')) {
        logoImg.src = "../Static/Imagen/Iconos/UNL-mediano-blanco.png";
    } else {
        logoImg.src = "../Static/Imagen/Iconos/Logo-UNL-mediano.png";
    }
    updateThemeToggleText();
    localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
}

function toggleUserOptions() {
    userOptionsMenu.style.display = userOptionsMenu.style.display === 'none' ? 'block' : 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        logoImg.src = "../Static/Imagen/Iconos/UNL-mediano-blanco.png";
    }
    updateThemeToggleText();

    themeToggle.addEventListener('click', function (e) {
        e.preventDefault();
        toggleTheme();
    });

    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', confirmLogout);
    }

    const backButton = document.querySelector('.btn-regresar');
    if (backButton) {
        backButton.addEventListener('click', function (event) {
            event.preventDefault();
            history.back();
        });
    }
});

document.addEventListener('click', function (event) {
    const userMenu = document.querySelector('.user-menu');
    if (!userMenu.contains(event.target) && userOptionsMenu.style.display === 'block') {
        userOptionsMenu.style.display = 'none';
    }
});