from Configuracion import datosUnaHoraArchivo, datosSeisMinutosArchivo, periodoConArchivoDeSeisMinutos, porcentajeMinimo
from Plots import MostrarDatos
from Transformacion import FrecuenciasAngularesOrdenadasPorImportancia
from Utilidades import LeerArchivo, GuardarCSV
from numpy import float64, ones, cos, sin, multiply, pi, arange, arctan
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
    resultados = FrecuenciasAngularesOrdenadasPorImportancia(listaDeDatos)[:n]

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
        nombreArchivoAGuardar = nombreArchivo[:-4] + "-frecuenciasImportantes.csv"
        GuardarCSV(nombreArchivoAGuardar, datos, informacionDeLosDatos)  

def PrediccionDeDatos(cantidadDeFrecuencias, datosX, datosY):
    frecuenciasImportantes = FrecuenciasAngularesOrdenadasPorImportancia(datosY)[:cantidadDeFrecuencias]
    cantidadDeDatos = len(datosX)
    funcionesPhi = [lambda x : multiply(ones(cantidadDeDatos), 1/2)]
    for frecuencia in frecuenciasImportantes:
        orden = int(frecuencia[1])
        funcionCos = lambda x, orden = orden : cos(multiply((2 * pi * orden) / cantidadDeDatos, x))
        funcionSin = lambda x, orden = orden : sin(multiply((2 * pi * orden) / cantidadDeDatos, x))

        funcionesPhi.append(funcionCos)
        funcionesPhi.append(funcionSin)

    vectorC = MinimosCuadrados(funcionesPhi, datosX, datosY)

    datosPredichos = FuncionEstrella(funcionesPhi, vectorC, datosX)
    errorCuadraticoMedio = ErrorCuadraticoMedio(funcionesPhi, vectorC, datosX, datosY)

    return datosPredichos, errorCuadraticoMedio 

def SeguirIterando(errorActual, errorAnterior, porcentaje):
    return abs(errorActual - errorAnterior) / abs(errorActual) > porcentaje / 100 


def CalculoDeAmplitudYFase(amplitudCoseno, amplitudSeno):
    fase = arctan(-amplitudSeno/amplitudCoseno)
    amplitud = amplitudCoseno/cos(fase)

    return fase, amplitud

def Main():
    #MostrarNFrecuenciasImportantes(datosUnaHoraArchivo, 20, 60, True)
    datosY = LeerArchivo(datosSeisMinutosArchivo)
    cantidadDatos = len(datosY)   
    datosX = arange(cantidadDatos)
    cantidadDeFunciones = 1

    frecuenciasImportantes = FrecuenciasAngularesOrdenadasPorImportancia(datosY)[:cantidadDeFunciones]  
    cantidadDeDatos = len(datosX)
    funcionesPhi = [lambda x : multiply(ones(cantidadDeDatos), 1/2)]
    for frecuencia in frecuenciasImportantes:
        orden = int(frecuencia[1])
        funcionCos = lambda x, orden = orden : cos(multiply((2 * pi * orden) / cantidadDeDatos, x))
        funcionSin = lambda x, orden = orden : sin(multiply((2 * pi * orden) / cantidadDeDatos, x))

        funcionesPhi.append(funcionCos)
        funcionesPhi.append(funcionSin)

    vectorC = MinimosCuadrados(funcionesPhi, datosX, datosY)
    amplitud, fase = CalculoDeAmplitudYFase(vectorC[1], vectorC[2])

    print(f"posicion media: {vectorC[0]}, amplitud: {amplitud}, fase: {fase}")

    '''
    predicciones, errorCuadraticoMedioAnterior = PrediccionDeDatos(cantidadDeFunciones, datosX, datosY)
    print(f"3, 3: ECM: {errorCuadraticoMedioAnterior}")
    cantidadDeFunciones += 1
    predicciones, errorCuadraticoMedioActual = PrediccionDeDatos(cantidadDeFunciones, datosX, datosY)
    print(f"5, 5: ECM: {errorCuadraticoMedioActual}")

    while SeguirIterando(errorCuadraticoMedioActual, errorCuadraticoMedioAnterior, porcentajeMinimo) and cantidadDeFunciones <= 20:

        cantidadDeFunciones += 1
        errorCuadraticoMedioAnterior = errorCuadraticoMedioActual
        predicciones, errorCuadraticoMedioActual = PrediccionDeDatos(cantidadDeFunciones, datosX, datosY)

        print(f"{1 + 2 * cantidadDeFunciones}, {1 + 2 * cantidadDeFunciones}: ECM: {errorCuadraticoMedioActual}")
        

    print(f"El error cuadratico medio es: {errorCuadraticoMedioActual}")
    print(f"Cantidad de funciones: {cantidadDeFunciones}")

    MostrarDatos(datosY, 1 / (10 * 24), titulo = "Original")
    MostrarDatos(predicciones, 1 / (10 * 24), titulo = "Prediccion")'''

if __name__ == "__main__":
    Main()