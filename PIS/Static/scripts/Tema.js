function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;
    updateThemeToggleText();
    updateLogo();
}

function getTheme() {
    return localStorage.getItem('theme') || 'light-mode';
}

function toggleTheme() {
    const currentTheme = getTheme();
    const newTheme = currentTheme === 'dark-mode' ? 'light-mode' : 'dark-mode';
    setTheme(newTheme);
}

function updateThemeToggleText() {
    const themeToggleText = document.querySelector('#theme-toggle span');
    if (themeToggleText) {
        themeToggleText.textContent = getTheme() === 'dark-mode' ? 'Modo claro' : 'Modo oscuro';
    }
}

function updateLogo() {
    const logoImg = document.getElementById('logo-img');
    if (logoImg) {
        logoImg.src = getTheme() === 'dark-mode'
            ? "../Static/Imagen/Iconos/UNL-mediano-blanco.png"
            : "../Static/Imagen/Iconos/Logo-UNL-mediano.png";
    }
}

function applyInitialTheme() {
    const savedTheme = getTheme();
    setTheme(savedTheme);
}

applyInitialTheme();

document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function (e) {
            e.preventDefault();
            toggleTheme();
        });
    }

    updateThemeToggleText();
    updateLogo();
});

function toggleUserOptions() {
    const userOptions = document.getElementById('user-options');
    if (userOptions) {
        userOptions.style.display = userOptions.style.display === 'block' ? 'none' : 'block';
    }
}

document.addEventListener('click', function (event) {
    const userOptions = document.getElementById('user-options');
    const username = document.querySelector('.username');
    if (userOptions && username && !username.contains(event.target)) {
        userOptions.style.display = 'none';
    }
});

function confirmLogout(event) {
    event.preventDefault();
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¿Deseas cerrar sesión?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cerrar sesión',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "{% url 'Cerrar_Sesion' %}";
        }
    });
}