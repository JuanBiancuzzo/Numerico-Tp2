from matplotlib import pyplot
from numpy import float64, ndarray, array, arange
from Configuracion import datosSeisMinutosArchivo, datosUnaHoraArchivo
from Transformacion import FrecuenciasAngulares, FrecuenciasAngularesOrdenadasPorImportancia, FuncinesPhi
from CuadradosMinimos import MinimosCuadrados, FuncionEstrella
from Utilidades import LeerArchivo

def Rango(inicio : float64, separacion : float64, cantidad : int) -> ndarray:
    resultado = []
    for i in range(cantidad):
        resultado.append(inicio + separacion * i)
    return array(resultado)


def GraficarDatos(datos : ndarray, separacion : float64, titulo = "", ejeX = "", ejeY = "", inicio = 0, logX = False, logY = False):
    rango = Rango(inicio, separacion, len(datos))
    GraficoContinuo(datos, rango, titulo, ejeX, ejeY, logX, logY)

def GraficarDatosBarra(datos : ndarray, separacion : float64, titulo = "", ejeX = "", ejeY = "", inicio = 0, logX = False, logY = False):
    rango = Rango(inicio, separacion, len(datos))
    GraficoDeBarra(datos, rango, titulo, ejeX, ejeY, logX, logY)


def GraficoContinuo(datos : ndarray, rango : ndarray, titulo, ejeX, ejeY, logX, logY):
    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    if logX: ax.set_xscale('log')
    if logY: ax.set_yscale('log')

    pyplot.title(titulo) 
    pyplot.xlabel(ejeX) 
    pyplot.ylabel(ejeY) 
    pyplot.plot(rango, datos)
    pyplot.grid(True)

def GraficoDeBarra(datos : ndarray, rango : ndarray, titulo, ejeX, ejeY, logX, logY):
    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    if logX: ax.set_xscale('log')
    if logY: ax.set_yscale('log')

    pyplot.title(titulo) 
    pyplot.xlabel(ejeX) 
    pyplot.ylabel(ejeY) 
    ax.bar(rango, datos)
    pyplot.grid(True)

def MostrarGraficos():
    pyplot.show()

def PrimerasFrecuenciasAngulares(datosDeAltura, cantidadMaxima):
    frecuenciasAngulares = FrecuenciasAngulares(datosDeAltura)
    frecuenciasAngularesConElModulo = []
    for frencuanciaAngular in frecuenciasAngulares:
        modulo = frencuanciaAngular[0]
        if len(frecuenciasAngularesConElModulo) < cantidadMaxima:
            frecuenciasAngularesConElModulo.append(modulo)
    return frecuenciasAngularesConElModulo

def Main():

    # datos en bruto

    datosAlturasMinutos = LeerArchivo(datosSeisMinutosArchivo)
    separacionMinutos = 1/(10 * 24)

    GraficarDatos(datosAlturasMinutos, separacionMinutos, "Datos en bruto de las alturas \n en el mes de enero", "Tiempo (dias)", "Altura (metros)")    

    datosAlturasHora = LeerArchivo(datosUnaHoraArchivo)
    separacionHora = 1/(24 * 30.5)

    GraficarDatos(datosAlturasHora, separacionHora, "Datos en bruto de las alturas \n en todo el año", "Tiempo (meses)", "Altura (metros)")
    
    MostrarGraficos()

    # frecuencias que se obtienen del fft

    frecuenciasDelMes = PrimerasFrecuenciasAngulares(datosAlturasMinutos, 300)
    frecuenciasDelAño = PrimerasFrecuenciasAngulares(datosAlturasHora, 500)
    
    GraficarDatosBarra(frecuenciasDelMes, 1, "Primeras frecuencias angulares\nen el mes", "Frecuencias angulares", "Relevancia", logY = True)
    GraficarDatosBarra(frecuenciasDelAño, 1, "Primeras frecuencias angulares\nen el año", "Frecuencias angulares", "Relevancia", logY = True)
    
    MostrarGraficos()

    # Comparacion entre datos y prediccion

    GraficarDatos(datosAlturasMinutos, separacionMinutos, "Datos en bruto de las alturas \n en el mes de enero", "Tiempo (dias)", "Altura (metros)")        

    cantidadDeDatos = len(datosAlturasMinutos)
    datosTiempo = arange(cantidadDeDatos)

    frecuenciasImportantes = FrecuenciasAngularesOrdenadasPorImportancia(datosAlturasMinutos)

    funcionesPhi = FuncinesPhi(frecuenciasImportantes[:1], cantidadDeDatos)
    amplitudesSerie = MinimosCuadrados(funcionesPhi, datosTiempo, datosAlturasMinutos)
    
    prediccionAlturasMinutos = FuncionEstrella(funcionesPhi, amplitudesSerie, datosTiempo)
    
    GraficarDatos(prediccionAlturasMinutos, separacionMinutos, "Prediccion de las alturas en el\nmes de enero con un solo termino", "Tiempo (dias)", "Altura (metros)")

    MostrarGraficos()

    GraficarDatos(datosAlturasHora, separacionHora, "Datos en bruto de las alturas \n en todo el año", "Tiempo (meses)", "Altura (metros)")
    
    cantidadDeDatos = len(datosAlturasHora)
    datosTiempo = arange(cantidadDeDatos)

    frecuenciasImportantes = FrecuenciasAngularesOrdenadasPorImportancia(datosAlturasHora)

    funcionesPhi = FuncinesPhi(frecuenciasImportantes[:7], cantidadDeDatos)
    amplitudesSerie = MinimosCuadrados(funcionesPhi, datosTiempo, datosAlturasHora)
    
    prediccionAlturasMinutos = FuncionEstrella(funcionesPhi, amplitudesSerie, datosTiempo) 

    GraficarDatos(datosAlturasHora, separacionHora, "Prediccion de las alturas en el\naño con 7 termino", "Tiempo (meses)", "Altura (metros)")

    MostrarGraficos()


if __name__ == "__main__":
    Main()