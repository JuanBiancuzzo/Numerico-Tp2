from matplotlib import pyplot
from numpy import float64, ndarray, array

def Rango(inicio : float64, separacion : float64, cantidad : int) -> ndarray:
    resultado = []
    for i in range(cantidad):
        resultado.append(inicio + separacion * i)
    return array(resultado)


def MostrarDatos(datos : ndarray, separacion : float64, titulo = "", ejeX = "", ejeY = ""):

    rango = Rango(0, separacion, len(datos))
    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    pyplot.title(titulo) 
    pyplot.xlabel(ejeX) 
    pyplot.ylabel(ejeY) 
    pyplot.plot(rango, datos)
    pyplot.grid(True)
    pyplot.show()