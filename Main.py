from Configuracion import datosUnaHoraArchivo, periodoConArchivoDeSeisMinutos
from Plots import MostrarDatos
from Transformacion import Transformada
from Utilidades import LeerArchivo, GuardarCSV
from numpy import float64, ones, cos, sin, multiply, pi
from CuadradosMinimos import MinimosCuadrados, FuncionEstrella, ErrorCuadraticoMedio

def CalcularPeriodo(periodoEnMinutos : float64):
    tipoDeDato = "min"

    if periodoEnMinutos / 60 > 1:
        tipoDeDato = "hora"
        periodoEnMinutos /= 60

        if periodoEnMinutos / 24 > 1:
            tipoDeDato = "dia"
            periodoEnMinutos /= 24

            if periodoEnMinutos / 30 > 1:
                tipoDeDato = "mes"
                periodoEnMinutos /= 30

    return periodoEnMinutos, tipoDeDato

def MostrarNFrecuenciasImportantes(nombreArchivo : str, n : int, relacionDatoMinutos : int, crearCSV : bool):
    listaDeDatos = LeerArchivo(nombreArchivo)
    cantidadDeDatosEnMinutos = len(listaDeDatos) * relacionDatoMinutos    
    resultados = Transformada(listaDeDatos, n)

    informacionDeLosDatos = ["Orden", "Periodo", "Tipo de periodo"]
    datos = []
    for resultado in resultados:
        orden = int(resultado[1])
        periodo = cantidadDeDatosEnMinutos / orden
        periodo, tipoDePeriodo = CalcularPeriodo(periodo)

        print(f"Orden: {orden}, con un periodo de {periodo} {tipoDePeriodo}")

        datoIndividual = [orden, periodo, tipoDePeriodo]
        datos.append(datoIndividual)
    
    if crearCSV:
        GuardarCSV(periodoConArchivoDeSeisMinutos, datos, informacionDeLosDatos)  


def Main():
    #MostrarNFrecuenciasImportantes(datosUnaHoraArchivo, 10, 60, False)
    #MostrarNFrecuenciasImportantes(datosSeisMinutosArchivo, 10, 6, False)

    datosX = []
    datosY = LeerArchivo(datosUnaHoraArchivo)
    separacion = 1
    cantidadDeFunciones = 20

    for i in range(len(datosY)):
        datosX.append(i * separacion)

    cantidadDatos = len(datosY)   
    frecuenciasImportantes = Transformada(datosY, cantidadDeFunciones)

    funcionesPhi = [lambda x : multiply(ones(cantidadDatos), 1/2)]
    for frecuencia in frecuenciasImportantes:
        orden = int(frecuencia[1])
        print(orden)
        funcionCos = lambda x, orden = orden : cos(multiply((2 * pi * orden) / cantidadDatos, x))
        funcionSin = lambda x, orden = orden : sin(multiply((2 * pi * orden) / cantidadDatos, x))

        funcionesPhi.append(funcionCos)
        funcionesPhi.append(funcionSin)

    vectorC = MinimosCuadrados(funcionesPhi, datosX, datosY)

    print(vectorC)

    datosPredichos = FuncionEstrella(funcionesPhi, vectorC, datosX)
    errorCuadraticoMedio = ErrorCuadraticoMedio(funcionesPhi, vectorC, datosX, datosY) 
    print(f"El error cuadratico medio es: {errorCuadraticoMedio}")

    MostrarDatos(datosY, 1 / (24))
    MostrarDatos(datosPredichos, 1 / (24))

if __name__ == "__main__":
    Main()