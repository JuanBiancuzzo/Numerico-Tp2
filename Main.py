from matplotlib.pyplot import setp
from numpy import multiply, ones, cos, sin, pi, arange
from Configuracion import datosSeisMinutosArchivo, datosUnaHoraArchivo, minutosPorDatoEnArchivoSeisMinutos, minutosPorDatoenArchivoUnaHora, porcentajeMinimo
from Transformacion import FrecuenciasAngularesOrdenadasPorImportancia, FuncinesPhi
from Utilidades import LeerArchivo
from CuadradosMinimos import MinimosCuadrados, CalculoDeAmplitudYFase, ErrorCuadraticoMedio

def CalcularPeriodo(periodoEnMinutos):
    tipoDeDato = "min"
    if periodoEnMinutos / 60 < 1:
        return periodoEnMinutos, tipoDeDato
    
    periodoEnHora = periodoEnMinutos / 60
    tipoDeDato = "hora"
    if periodoEnHora / 24 < 1:
        return periodoEnHora, tipoDeDato

    periodoEnDia = periodoEnHora / 24
    tipoDeDato = "dia"
    if periodoEnDia / 30 < 1:
        return periodoEnDia, tipoDeDato

    periodoEnMes = periodoEnDia / 30
    tipoDeDato = "mes"
    return periodoEnMes, tipoDeDato

def MostrarFrecuenciasImportantes(frecuenciasImportantes, cantidadDeFrecuencias, cantidadDeDatos, minutosPorDato):
    frecuencias = frecuenciasImportantes[:cantidadDeFrecuencias]
    for frecuencia in frecuencias:
        frecuenciaAngular = int(frecuencia[1])
        periodo = (cantidadDeDatos * minutosPorDato) / frecuenciaAngular
        periodo, tipoDePeriodo = CalcularPeriodo(periodo)

        print(f"Frecuencia angular: {frecuenciaAngular}, con un periodo de {periodo} {tipoDePeriodo}")

def DatosDeLaSerie(amplitudesDeLaSerie):

    datosDeLaSerie = [amplitudesDeLaSerie[0]]
    for i in range(1, len(amplitudesDeLaSerie[1:]), 2):
        amplitudCoseno = amplitudesDeLaSerie[i]
        amplitudSeno = amplitudesDeLaSerie[i + 1]

        amplitud, fase = CalculoDeAmplitudYFase(amplitudCoseno, amplitudSeno)
        datosDeLaSerie.append(amplitud)
        datosDeLaSerie.append(fase)

    return datosDeLaSerie

def MostrarDatosDeLaSerie(datosDeLaSerie):
    posicionMedia3Digitos = "{0:.3f}".format(datosDeLaSerie[0])
    print(f"Posicion media: {posicionMedia3Digitos}")
    for i in range(1, len(datosDeLaSerie[1:]), 2):
        amplitud = datosDeLaSerie[i]
        fase = datosDeLaSerie[i + 1]
        posicion = (i + 1) // 2
        amplitudCon3Digitos = "{0:.3f}".format(amplitud)
        faseCon3Digitos = "{0:.3f}".format(fase)
        print(f"Amplitud {posicion}: {amplitudCon3Digitos}, Fase {posicion}: {faseCon3Digitos}")

def CalculoDelError(cantidadDeTerminos, datosTiempo, datosAltura):
    cantidadDeDatos = len(datosAltura)
    frecuenciasImportantes = FrecuenciasAngularesOrdenadasPorImportancia(datosAltura)
    funcinesPhi = FuncinesPhi(frecuenciasImportantes[:cantidadDeTerminos], cantidadDeDatos)
    amplitudesSerie = MinimosCuadrados(funcinesPhi, datosTiempo, datosAltura)
    return ErrorCuadraticoMedio(funcinesPhi, amplitudesSerie, datosTiempo, datosAltura)

def MostrarErrorCuadraticoMedio(cantidadDeTerminos, errorCuadraticoMedio):
    tamanioDeLaMatriz = 1 + 2 * cantidadDeTerminos
    print(f"{tamanioDeLaMatriz}x{tamanioDeLaMatriz}: ECM: {errorCuadraticoMedio}")

def SeguirIterando(errorActual, errorAnterior, porcentaje):
    return abs(errorActual - errorAnterior) / abs(errorActual) > porcentaje / 100 

def Main():
    print("Parte 1) \n\tDatos del mes\n")

    datosAltura = LeerArchivo(datosSeisMinutosArchivo)
    cantidadDeDatos = len(datosAltura)
    datosTiempo = arange(cantidadDeDatos)

    frecuenciasImportantes = FrecuenciasAngularesOrdenadasPorImportancia(datosAltura)

    MostrarFrecuenciasImportantes(frecuenciasImportantes, 1, cantidadDeDatos, minutosPorDatoEnArchivoSeisMinutos)

    funcionesPhi = FuncinesPhi(frecuenciasImportantes[:1], cantidadDeDatos)
    amplitudesSerie = MinimosCuadrados(funcionesPhi, datosTiempo, datosAltura)

    datosDeLaSerie = DatosDeLaSerie(amplitudesSerie)
    MostrarDatosDeLaSerie(datosDeLaSerie)

    print("\nParte 2) \n\tDatos del año\n")

    datosAltura = LeerArchivo(datosUnaHoraArchivo)
    cantidadDeDatos = len(datosAltura)
    datosTiempo = arange(cantidadDeDatos)

    frecuenciasImportantes = FrecuenciasAngularesOrdenadasPorImportancia(datosAltura)

    MostrarFrecuenciasImportantes(frecuenciasImportantes, 1, cantidadDeDatos, minutosPorDatoenArchivoUnaHora)

    funcionesPhi = FuncinesPhi(frecuenciasImportantes[:1], cantidadDeDatos)
    amplitudesSerie = MinimosCuadrados(funcionesPhi, datosTiempo, datosAltura)

    datosDeLaSerie = DatosDeLaSerie(amplitudesSerie)
    MostrarDatosDeLaSerie(datosDeLaSerie)

    cantidadDeTerminos = 1
    errorCuadraticoMedioAnterior = CalculoDelError(cantidadDeTerminos, datosTiempo, datosAltura)
    MostrarErrorCuadraticoMedio(cantidadDeTerminos, errorCuadraticoMedioAnterior)
    
    cantidadDeTerminos += 1
    errorCuadraticoMedioActual = CalculoDelError(cantidadDeTerminos, datosTiempo, datosAltura)
    MostrarErrorCuadraticoMedio(cantidadDeTerminos, errorCuadraticoMedioActual)

    while SeguirIterando(errorCuadraticoMedioActual, errorCuadraticoMedioAnterior, porcentajeMinimo) and cantidadDeTerminos <= 20:

        cantidadDeTerminos += 1
        errorCuadraticoMedioAnterior = errorCuadraticoMedioActual
        errorCuadraticoMedioActual = CalculoDelError(cantidadDeTerminos, datosTiempo, datosAltura)
        MostrarErrorCuadraticoMedio(cantidadDeTerminos, errorCuadraticoMedioActual)

    print(f"El error cuadratico medio de ", end = "")
    MostrarErrorCuadraticoMedio(cantidadDeTerminos, errorCuadraticoMedioActual)

    print("\nLa informacion final dio: ")
    frecuenciasImportantes = FrecuenciasAngularesOrdenadasPorImportancia(datosAltura)
    funcinesPhi = FuncinesPhi(frecuenciasImportantes[:cantidadDeTerminos], cantidadDeDatos)
    amplitudesSerie = MinimosCuadrados(funcinesPhi, datosTiempo, datosAltura)
    datosDeLaSerie = DatosDeLaSerie(amplitudesSerie)
    MostrarDatosDeLaSerie(datosDeLaSerie)
    MostrarFrecuenciasImportantes(frecuenciasImportantes, cantidadDeTerminos, cantidadDeDatos, minutosPorDatoenArchivoUnaHora)

if __name__ == "__main__":
    Main()