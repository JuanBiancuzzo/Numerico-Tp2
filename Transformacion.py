from numpy import fft, ndarray, linalg, array

def Transformada(datos : ndarray, cantidadFrecuencias : int) -> ndarray:
    vectoresComplejos = fft.fft(datos)
    frecuencias = []

    for posicion, vector in enumerate(vectoresComplejos): 
        modulo = linalg.norm(vector)
        frecuencias.append((modulo, posicion))

    frecuenciasImportantes = frecuencias[1:len(frecuencias)//2]

    frecuenciasImportantes.sort(reverse = True, key = lambda valor: valor[0])
    return array(frecuenciasImportantes[:cantidadFrecuencias])
