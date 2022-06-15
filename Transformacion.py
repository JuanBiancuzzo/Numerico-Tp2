from numpy import fft, ndarray, linalg, array, multiply, ones, cos, sin, pi

def FrecuenciasAngulares(datos : ndarray) -> ndarray:
    vectoresComplejos = fft.fft(datos)
    frecuencias = []

    for posicion, vector in enumerate(vectoresComplejos): 
        modulo = linalg.norm(vector)
        frecuencias.append((modulo, posicion))

    return frecuencias[:len(frecuencias)//2]

def FrecuenciasAngularesOrdenadasPorImportancia(datos : ndarray) -> ndarray:
    frecuenciasImportantes = FrecuenciasAngulares(datos)[1:]
    frecuenciasImportantes.sort(reverse = True, key = lambda valor: valor[0])
    return array(frecuenciasImportantes)

def FuncinesPhi(frecuenciasImportantes, cantidadDeDatos):
    funcionesPhi = [lambda x : multiply(ones(cantidadDeDatos), 1/2)]
    for frecuencia in frecuenciasImportantes:
        orden = int(frecuencia[1])
        funcionCos = lambda x, orden = orden : cos(multiply((2 * pi * orden) / cantidadDeDatos, x))
        funcionSin = lambda x, orden = orden : sin(multiply((2 * pi * orden) / cantidadDeDatos, x))

        funcionesPhi.append(funcionCos)
        funcionesPhi.append(funcionSin)    
    return funcionesPhi