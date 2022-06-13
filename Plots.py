from matplotlib import pyplot
from numpy import float64, ndarray, array

def Rango(inicio : float64, separacion : float64, cantidad : int) -> ndarray:
    resultado = []
    for i in range(cantidad):
        resultado.append(inicio + separacion * i)
    return array(resultado)


def MostrarDatos(datos : ndarray, separacion : float64, inicio = 0, titulo = "", ejeX = "", ejeY = "", logX = False, logY = False):

    rango = Rango(inicio, separacion, len(datos))
    Grafico(datos, rango, titulo, ejeX, ejeY, logX, logY)


def Grafico(datos : ndarray, rango : ndarray, titulo = "", ejeX = "", ejeY = "", logX = False, logY = False):
    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    if logX:
        ax.set_xscale('log')
    if logY:
        ax.set_yscale('log')

    pyplot.title(titulo) 
    pyplot.xlabel(ejeX) 
    pyplot.ylabel(ejeY) 
    pyplot.plot(rango, datos)
    pyplot.grid(True)
    pyplot.show()