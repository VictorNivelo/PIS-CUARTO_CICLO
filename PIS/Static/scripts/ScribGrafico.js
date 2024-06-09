let cantidadLeyendas;
var arregloDatos = [];

function agregarDato() {
    cantidadLeyendas = document.getElementsByClassName("dato").length;
    cantidadLeyendas++;

    const dato = document.createElement("div");
    dato.className = "mb-3 row dato";

    const col8 = document.createElement("div");
    col8.className = "col-8";
    const inputLeyenda = document.createElement("input");
    inputLeyenda.type = "text";
    inputLeyenda.className = "form-control serie";
    inputLeyenda.placeholder = "Nombre";
    col8.appendChild(inputLeyenda);

    const col4 = document.createElement("div");
    col4.className = "col-4";
    const inputValor = document.createElement("input");
    inputValor.type = "text";
    inputValor.className = "form-control valor";
    inputValor.placeholder = "Valor";
    col4.appendChild(inputValor);

    dato.appendChild(col8);
    dato.appendChild(col4);
    document.getElementById("datos").appendChild(dato);
}

function cargarGrafico() {
    google.charts.load('current', {
        'packages': ['corechart']
    });
    google.charts.setOnLoadCallback(drawChart);
}

function drawChart() {
    arregloDatos = [];
    var datos = document.getElementById("datos").getElementsByTagName("input");

    for (let i = 0; i < datos.length; i++) {
        if (datos[i].value === "") {
            alert("Ingrese toda la información para poder graficar.");
            return;
        }
    }
    arregloDatos.push(['Gráfico', '']);

    for (let i = 0; i < datos.length; i += 2) {
        arregloDatos.push([datos[i].value, parseInt(datos[i + 1].value)]);
    }

    var data = google.visualization.arrayToDataTable(arregloDatos);
    var options = {
        'title': document.getElementById("titulo").value,
        'width': 600,
        'height': 400
    };

    var chart;
    if (document.getElementById("tipo").value == "circular") {
        chart = new google.visualization.PieChart(document.getElementById('piechart'));
    } else {
        chart = new google.visualization.ColumnChart(document.getElementById('piechart'));
    }
    chart.draw(data, options);
}
