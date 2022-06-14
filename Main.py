from numpy import arange
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
    if periodoEnMes / 12 < 1:
        return periodoEnMes, tipoDeDato

    periodoEnAnio = periodoEnMes / 12
    tipoDeDato = "año"
    return periodoEnAnio, tipoDeDato

def MostrarFrecuenciasImportantes(frecuenciasImportantes, cantidadDeFrecuencias, cantidadDeDatos, minutosPorDato):
    frecuencias = frecuenciasImportantes[:cantidadDeFrecuencias]
    for frecuencia in frecuencias:
        frecuenciaAngular = int(frecuencia[1])
        periodo = (cantidadDeDatos * minutosPorDato) / frecuenciaAngular
        periodo, tipoDePeriodo = CalcularPeriodo(periodo)

        periodoCon3Digitos = "{0:.3f}".format(periodo)
        print(f"Frecuencia angular: {frecuenciaAngular}, con un periodo de {periodoCon3Digitos} {tipoDePeriodo}")

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
    errorCon3Decimales = "{0:.3f}".format(errorCuadraticoMedio)
    print(f"{tamanioDeLaMatriz}x{tamanioDeLaMatriz}: ECM: {errorCon3Decimales}")

def SeguirIterando(errorActual, errorAnterior, porcentaje):
    return abs(errorActual - errorAnterior) / abs(errorActual) > porcentaje / 100 

def Main():
    print("Parte 1) \n\tDatos del mes\n")

    datosAltura = LeerArchivo(datosSeisMinutosArchivo)
    cantidadDeDatos = len(datosAltura)
    datosTiempo = arange(cantidadDeDatos)
    cantidadDeTerminos = 1

    frecuenciasImportantes = FrecuenciasAngularesOrdenadasPorImportancia(datosAltura)

    MostrarFrecuenciasImportantes(frecuenciasImportantes, cantidadDeTerminos, cantidadDeDatos, minutosPorDatoEnArchivoSeisMinutos)

    funcionesPhi = FuncinesPhi(frecuenciasImportantes[:cantidadDeTerminos], cantidadDeDatos)
    amplitudesSerie = MinimosCuadrados(funcionesPhi, datosTiempo, datosAltura)

    datosDeLaSerie = DatosDeLaSerie(amplitudesSerie)
    MostrarDatosDeLaSerie(datosDeLaSerie)

    errorCuadraticoMedio = CalculoDelError(cantidadDeTerminos, datosTiempo, datosAltura)
    MostrarErrorCuadraticoMedio(cantidadDeTerminos, errorCuadraticoMedio)

    print("\nParte 2) \n\tDatos del año\n")

    datosAltura = LeerArchivo(datosUnaHoraArchivo)
    cantidadDeDatos = len(datosAltura)
    datosTiempo = arange(cantidadDeDatos)

    frecuenciasImportantes = FrecuenciasAngularesOrdenadasPorImportancia(datosAltura)

    MostrarFrecuenciasImportantes(frecuenciasImportantes, cantidadDeTerminos, cantidadDeDatos, minutosPorDatoenArchivoUnaHora)

    funcionesPhi = FuncinesPhi(frecuenciasImportantes[:cantidadDeTerminos], cantidadDeDatos)
    amplitudesSerie = MinimosCuadrados(funcionesPhi, datosTiempo, datosAltura)

    datosDeLaSerie = DatosDeLaSerie(amplitudesSerie)
    MostrarDatosDeLaSerie(datosDeLaSerie)

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