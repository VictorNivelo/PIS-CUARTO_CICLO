let cantidadLeyendas;

var arregloDatos = [];

function agregarDato() {
    cantidadLeyendas = document.getElementsByClassName("dato").length;
    cantidadLeyendas++;

    const dato = document.createElement("div");
    dato.className = "dato";

    const inputLeyenda = document.createElement("input");
    inputLeyenda.type = "text";
    inputLeyenda.className = "serie";
    inputLeyenda.placeholder = "Nombre"
    dato.appendChild(inputLeyenda);
    document.getElementById("datos").appendChild(dato);

    const inputValor = document.createElement("input");
    inputValor.type = "text";
    inputValor.className = "valor";
    inputValor.placeholder = "Valor ";
    dato.appendChild(inputValor);
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
    for (i = 0; i < datos.length; i++) {
        if (datos[i].value === "") {
            alert("Porfavor ingrese todos los datos");
            return;
        }
    }
    var t = ['Gráfico', ''];
    arregloDatos.push(t);

    for (i = 0; i < datos.length; i = i + 2) {
        t = [datos[i].value, parseInt(datos[i + 1].value)];
        arregloDatos.push(t);
    }

    var data = google.visualization.arrayToDataTable(arregloDatos);

    var options = {
        'title': document.getElementById("titulo").value,
        'width': 600,
    };

    if (document.getElementById("tipo").value == "circular") {
        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);
    } else {
        var chart = new google.visualization.ColumnChart(document.getElementById('piechart'));
        chart.draw(data, options);
    }

}