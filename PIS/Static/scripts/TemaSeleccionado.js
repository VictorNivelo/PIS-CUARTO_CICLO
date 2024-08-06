const themeToggle = document.getElementById('theme-toggle');
const logoImg = document.getElementById('logo-img');

function updateThemeToggleText() {
    const themeToggleText = document.querySelector('#theme-toggle');
    if (document.body.classList.contains('dark-mode')) {
        themeToggleText.innerHTML = '<i class="fas fa-sun"></i> Modo Claro';
    } else {
        themeToggleText.innerHTML = '<i class="fas fa-moon"></i> Modo Oscuro';
    }
}

themeToggle.addEventListener('click', function (e) {
    e.preventDefault();
    document.body.classList.toggle('dark-mode');
    if (document.body.classList.contains('dark-mode')) {
        logoImg.src = "../Static/Imagen/Iconos/UNL-mediano-blanco.png";
    } else {
        logoImg.src = "../Static/Imagen/Iconos/Logo-UNL-mediano.png";
    }
    updateThemeToggleText();
});

function toggleUserOptions() {
    const userOptions = document.getElementById('user-options');
    const isExpanded = userOptions.style.display === 'block';
    userOptions.style.display = isExpanded ? 'none' : 'block';
    document.querySelector('.username').setAttribute('aria-expanded', !isExpanded);
    updateThemeToggleText();
}

document.addEventListener('DOMContentLoaded', function () {
    updateThemeToggleText();
});