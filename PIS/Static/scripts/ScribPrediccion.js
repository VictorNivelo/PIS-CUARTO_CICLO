function resetForm() {
    document.getElementById("form-grafico").reset();
}

function cargarGrafico() {
    google.charts.load('current', { 'packages': ['corechart'] });
    google.charts.setOnLoadCallback(drawChart);
}

function drawChart() {
    const genero = document.getElementById("genero").value;
    const matriculados = parseInt(document.getElementById("matriculados").value);
    const desertores = parseInt(document.getElementById("desertores").value);
    const reprobados = parseInt(document.getElementById("reprobados").value);
    const aprobados = parseInt(document.getElementById("aprobados").value);

    if (isNaN(matriculados) || isNaN(desertores) || isNaN(reprobados) || isNaN(aprobados)) {
        alert("Ingrese todos los valores necesarios para generar el gráfico.");
        return;
    }

    const data = google.visualization.arrayToDataTable([
        ['Estado', 'Cantidad'],
        ['Desertores', desertores],
        ['Reprobados', reprobados],
        ['Aprobados', aprobados]
    ]);

    const options = {
        title: `Estado de Estudiantes (${genero === 'todos' ? 'Todos los géneros' : genero.charAt(0).toUpperCase() + genero.slice(1)})`,
        width: 700,
        height: 500
    };

    const chart = new google.visualization.PieChart(document.getElementById('piechart'));
    chart.draw(data, options);
}

function actualizarValores() {
    const matriculados = parseInt(document.getElementById("matriculados").value);
    const desertores = document.getElementById("desertores");
    const reprobados = document.getElementById("reprobados");
    const aprobados = document.getElementById("aprobados");

    if (!isNaN(matriculados)) {
        desertores.max = reprobados.max = aprobados.max = matriculados;
    }
}

function validarSuma() {
    const matriculados = parseInt(document.getElementById("matriculados").value);
    const desertores = parseInt(document.getElementById("desertores").value);
    const reprobados = parseInt(document.getElementById("reprobados").value);
    const aprobados = parseInt(document.getElementById("aprobados").value);

    if (desertores + reprobados + aprobados > matriculados) {
        alert("La suma de desertores, reprobados y aprobados no puede exceder el número de matriculados.");
    }
}
