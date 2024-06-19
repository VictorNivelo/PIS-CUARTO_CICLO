def BusquedaBinaria(lista, valor):
    inicio = 0
    fin = len(lista) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if lista[medio] == valor:
            return medio
        elif lista[medio] < valor:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1


def BusquedaLineal(lista, valor):
    for i in range(len(lista)):
        if lista[i] == valor:
            return i
    return -1


def ordenarLista(lista):
    return sorted(lista)


def cargarCombo(combo, lista):
    combo.clear()
    for i in lista:
        combo.addItem(i)


def GuardarArchivo(nombreArchivo, datos):
    archivo = open(nombreArchivo, "w")
    archivo.write(datos)
    archivo.close()


def LeerArchivo(nombreArchivo):
    archivo = open(nombreArchivo, "r")
    datos = archivo.read()
    archivo.close()
    return datos


def GuardarLista(nombreArchivo, lista):
    archivo = open(nombreArchivo, "w")
    for i in lista:
        archivo.write(i + "\n")
    archivo.close()


def LeerLista(nombreArchivo):
    archivo = open(nombreArchivo, "r")
    lista = archivo.readlines()
    archivo.close()
    return lista


def GuardarDiccionario(nombreArchivo, diccionario):
    archivo = open(nombreArchivo, "w")
    for i in diccionario:
        archivo.write(i + "," + diccionario[i] + "\n")
    archivo.close()


def LeerDiccionario(nombreArchivo):
    archivo = open(nombreArchivo, "r")
    diccionario = {}
    for linea in archivo:
        linea = linea[:-1]
        datos = linea.split(",")
        diccionario[datos[0]] = datos[1]
    archivo.close()
    return diccionario


def BusquedaEnProfundidad(grafo, inicio, visitados):
    visitados.append(inicio)
    for i in grafo[inicio]:
        if i not in visitados:
            BusquedaEnProfundidad(grafo, i, visitados)
    return visitados


def AgregarRoles(grafo, inicio, visitados):
    visitados.append(inicio)
    for i in grafo[inicio]:
        if i not in visitados:
            AgregarRoles(grafo, i, visitados)
    return visitados


def AgregarGeneros(grafo, inicio, visitados):
    visitados.append(inicio)
    for i in grafo[inicio]:
        if i not in visitados:
            AgregarGeneros(grafo, i, visitados)
    return visitados


def AgregarDNI(grafo, inicio, visitados):
    visitados.append(inicio)
    for i in grafo[inicio]:
        if i not in visitados:
            AgregarDNI(grafo, i, visitados)
    return visitados


def EliminarRoles(grafo, inicio, visitados):
    visitados.append(inicio)
    for i in grafo[inicio]:
        if i not in visitados:
            EliminarRoles(grafo, i, visitados)
    return visitados


def EliminarGeneros(grafo, inicio, visitados):
    visitados.append(inicio)
    for i in grafo[inicio]:
        if i not in visitados:
            EliminarGeneros(grafo, i, visitados)
    return visitados


def EliminarDNI(grafo, inicio, visitados):
    visitados.append(inicio)
    for i in grafo[inicio]:
        if i not in visitados:
            EliminarDNI(grafo, i, visitados)
    return visitados


def BusquedaEnAnchura(grafo, inicio):
    visitados = []
    cola = []
    visitados.append(inicio)
    cola.append(inicio)
    while len(cola) > 0:
        nodo = cola.pop(0)
        for i in grafo[nodo]:
            if i not in visitados:
                visitados.append(i)
                cola.append(i)
    return visitados


def BusquedaEnAnchura2(grafo, inicio):
    visitados = []
    cola = []
    visitados.append(inicio)
    cola.append(inicio)
    while len(cola) > 0:
        nodo = cola.pop(0)
        for i in grafo[nodo]:
            if i not in visitados:
                visitados.append(i)
                cola.append(i)
    return visitados


def BusquedaEnAnchura3(grafo, inicio):
    visitados = []
    cola = []
    visitados.append(inicio)
    cola.append(inicio)
    while len(cola) > 0:
        nodo = cola.pop(0)
        for i in grafo[nodo]:
            if i not in visitados:
                visitados.append(i)
                cola.append(i)
    return visitados
