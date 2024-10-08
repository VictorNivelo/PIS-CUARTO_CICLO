# <script>
#         document.getElementById('btnRegresar').addEventListener('click', function () {
#             Swal.fire({
#                 title: '¿Estás seguro?',
#                 text: "¡Se perderán los datos no guardados!",
#                 icon: 'warning',
#                 showCancelButton: true,
#                 confirmButtonColor: '#3085d6',
#                 cancelButtonColor: '#d33',
#                 confirmButtonText: 'Sí, regresar',
#                 cancelButtonText: 'Cancelar'
#             }).then((result) => {
#                 if (result.isConfirmed) {
#                     var paginaAnterior = localStorage.getItem('paginaAnterior');
#                     if (paginaAnterior) {
#                         window.location.href = paginaAnterior;
#                     } else {
#                         window.location.href = '/';
#                     }
#                 }
#             });
#         });

#         function recordarPaginaAnterior() {
#             localStorage.setItem('paginaAnterior', document.referrer);
#         }

#         function soloLetras(e) {
#             var key = e.keyCode || e.which;
#             var tecla = String.fromCharCode(key).toLowerCase();
#             var letras = " áéíóúabcdefghijklmnñopqrstuvwxyz";
#             var especiales = "8-37-39-46";

#             var tecla_especial = false
#             for (var i in especiales) {
#                 if (key == especiales[i]) {
#                     tecla_especial = true;
#                     break;
#                 }
#             }

#             if (letras.indexOf(tecla) == -1 && !tecla_especial) {
#                 Swal.fire({
#                     icon: 'error',
#                     title: 'Error',
#                     text: 'Solo se permiten letras en este campo',
#                 });
#                 return false;
#             }
#         }

#         function soloNumeros(e) {
#             var key = e.keyCode || e.which;
#             var tecla = String.fromCharCode(key);
#             var numeros = "0123456789";

#             if (numeros.indexOf(tecla) == -1) {
#                 Swal.fire({
#                     icon: 'error',
#                     title: 'Error',
#                     text: 'Solo se permiten números en este campo',
#                 });
#                 return false;
#             }
#         }

#         function validarLongitud(input, longitud, nombreCampo) {
#             if (input.value.length !== longitud) {
#                 Swal.fire({
#                     icon: 'error',
#                     title: 'Error',
#                     text: `El ${nombreCampo} debe tener exactamente ${longitud} dígitos.`,
#                 });
#                 return false;
#             }
#             return true;
#         }

#         function validarContrasenia(password) {
#             var regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/;
#             return regex.test(password);
#         }

#         function validarTelefono(telefono) {
#             return telefono.startsWith('09') && telefono.length === 10;
#         }

#         document.getElementById('id_first_name').onkeypress = soloLetras;
#         document.getElementById('id_last_name').onkeypress = soloLetras;
#         document.getElementById('id_telefono').onkeypress = soloNumeros;
#         document.getElementById('id_dni').onkeypress = soloNumeros;

#         document.getElementById('id_password1').addEventListener('input', function () {
#             var password = this.value;
#             if (password && !validarContrasenia(password)) {
#                 this.setCustomValidity('La contraseña debe tener al menos 8 caracteres, incluyendo una mayúscula, una minúscula y un número.');
#             } else {
#                 this.setCustomValidity('');
#             }
#         });

#         document.getElementById('id_telefono').addEventListener('input', function () {
#             if (!validarTelefono(this.value)) {
#                 this.setCustomValidity('El número de teléfono debe comenzar con 09 y tener 10 dígitos');
#             } else {
#                 this.setCustomValidity('');
#             }
#         });

#         document.getElementById('id_dni').addEventListener('input', function () {
#             if (this.value.length !== 10) {
#                 this.setCustomValidity('El DNI debe tener exactamente 10 dígitos');
#             } else {
#                 this.setCustomValidity('');
#             }
#         });

#         document.getElementById('registerForm').onsubmit = function (e) {
#             e.preventDefault();

#             var password1 = document.getElementById('id_password1').value;
#             var password2 = document.getElementById('id_password2').value;
#             var telefono = document.getElementById('id_telefono').value;
#             var dni = document.getElementById('id_dni').value;

#             if (!validarContrasenia(password1)) {
#                 Swal.fire({
#                     icon: 'error',
#                     title: 'Contraseña no segura',
#                     text: 'La contraseña debe tener al menos 8 caracteres, incluyendo una mayúscula, una minúscula y un número.',
#                 });
#                 return false;
#             }

#             if (password1 !== password2) {
#                 Swal.fire({
#                     icon: 'error',
#                     title: 'Error',
#                     text: 'Las contraseñas no coinciden',
#                 });
#                 return false;
#             }

#             if (!validarTelefono(telefono)) {
#                 Swal.fire({
#                     icon: 'error',
#                     title: 'Error',
#                     text: 'El número de teléfono debe comenzar con 09 y tener 10 dígitos',
#                 });
#                 return false;
#             }

#             if (!validarLongitud(document.getElementById('id_dni'), 10, 'DNI')) {
#                 return false;
#             }

#             var inputs = this.querySelectorAll('input, select');
#             for (var i = 0; i < inputs.length; i++) {
#                 if (!inputs[i].value) {
#                     Swal.fire({
#                         icon: 'error',
#                         title: 'Error',
#                         text: 'Por favor, complete todos los campos',
#                     });
#                     return false;
#                 }
#             }

#             var formData = new FormData(this);
#             var jsonData = {};
#             formData.forEach((value, key) => { jsonData[key] = value });

#             fetch('{% url "Registrar_Usuario" %}', {
#                 method: 'POST',
#                 headers: {
#                     'Content-Type': 'application/json',
#                     'X-CSRFToken': '{{ csrf_token }}'
#                 },
#                 body: JSON.stringify(jsonData)
#             })
#                 .then(response => response.json())
#                 .then(data => {
#                     if (data.status === 'success') {
#                         Swal.fire({
#                             title: 'Éxito',
#                             text: data.message,
#                             icon: 'success',
#                             confirmButtonText: 'OK'
#                         }).then((result) => {
#                             if (result.isConfirmed) {
#                                 window.location.href = '{% url "Iniciar_Sesion" %}';
#                             }
#                         });
#                     } else {
#                         let errorMessage = data.message;
#                         if (data.errors) {
#                             errorMessage += '\n' + data.errors.join('\n');
#                         }
#                         Swal.fire({
#                             title: 'Error',
#                             text: errorMessage,
#                             icon: 'error',
#                             confirmButtonText: 'OK'
#                         });
#                     }
#                 })
#                 .catch(error => {
#                     console.error('Error:', error);
#                     Swal.fire({
#                         title: 'Error',
#                         text: 'Hubo un problema al procesar su solicitud.',
#                         icon: 'error',
#                         confirmButtonText: 'OK'
#                     });
#                 });
#         };

#         window.onload = recordarPaginaAnterior;
#     </script>


#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');

#         html,
#         body {
#             height: 100%;
#             margin: 0;
#             padding: 0;
#         }

#         body {
#             background: url('../Static/Imagen/b.png') no-repeat center center fixed;
#             background-size: cover;
#             font-family: Arial, sans-serif;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#         }

#         .caja {
#             background: rgba(255, 255, 255, 0.9);
#             border-radius: 10px;
#             box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
#             width: 100%;
#             max-width: 600px;
#             padding: 30px;
#             margin: auto;
#         }

#         .form-wrapper {
#             padding: 20px;
#         }

#         .t {
#             font-family: 'Lobster', cursive;
#             text-align: center;
#             margin-bottom: 30px;
#             color: #333;
#         }

#         .form-group {
#             margin-bottom: 20px;
#         }

#         label {
#             color: #555;
#             font-weight: bold;
#         }

#         input[type="text"],
#         input[type="email"],
#         input[type="password"],
#         input[type="date"],
#         input[type="tel"],
#         select {
#             width: 100%;
#             padding: 10px;
#             border: 1px solid #ccc;
#             border-radius: 5px;
#             font-size: 16px;
#             margin-top: 5px;
#             color: #333;
#             box-sizing: border-box;
#         }

#         input[type="text"],
#         input[type="email"],
#         input[type="password"],
#         input[type="date"],
#         input[type="tel"],
#         select {
#             height: 40px;
#         }

#         select option {
#             color: initial;
#         }

#         input::placeholder,
#         select::placeholder {
#             color: #aaa;
#         }

#         input.has-value,
#         select.has-value {
#             color: #333;
#         }

#         button[type="submit"],
#         .btn-regresar {
#             width: calc(50% - 5px);
#             padding: 10px;
#             border: none;
#             border-radius: 5px;
#             font-size: 16px;
#             cursor: pointer;
#             transition: background-color 0.3s;
#             margin-top: 10px;
#         }

#         button[type="submit"] {
#             background-color: #4CAF50;
#             color: white;
#         }

#         button[type="submit"]:hover {
#             background-color: #45a049;
#         }

#         .btn-regresar {
#             background-color: #f0ad4e;
#             color: white;
#         }

#         .btn-regresar:hover {
#             background-color: #eea236;
#         }

#         .button-group {
#             display: flex;
#             justify-content: space-between;
#             margin-top: 20px;
#         }

#         .button-group button {
#             margin-top: 0;
#         }

#         ::placeholder,
#         select:invalid,
#         input[type="date"]:invalid {
#             color: #999 !important;
#         }

#         input,
#         select,
#         input[type="date"] {
#             color: #999;
#         }

#         input:focus,
#         select:focus,
#         input[type="date"]:focus,
#         input:not(:placeholder-shown),
#         select:not(:invalid),
#         input[type="date"]:not(:invalid) {
#             color: #000 !important;
#         }

#         select option {
#             color: #000;
#         }

#         select option:first-child {
#             color: #999;
#         }

#         input[type="date"]:not(:valid):not(:focus) {
#             color: #999;
#         }

#         .col-md-6 {
#             width: 50%;
#             float: left;
#             padding-right: 15px;
#             box-sizing: border-box;
#         }

#         .col-md-6:nth-child(even) {
#             padding-right: 0;
#         }

#         .row:after {
#             content: "";
#             display: table;
#             clear: both;
#         }
#     </style>
