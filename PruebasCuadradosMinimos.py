import numpy
import CuadradosMinimos

class Output:
    def __init__(self, estado : bool, mensaje : str):
        self.estado = estado
        self.mensaje = mensaje

    def __str__(self):
        mensajeEstado = "Exito" if self.estado else "Error"
        return mensajeEstado + ": " + self.mensaje

def CompararFloat(esperado : float, obtenido : float) -> bool:
    epsilon = 0.001
    return esperado - epsilon < obtenido < esperado + epsilon

def PruebaFuncionLinealTieneCuadradosMinimosPerfectosContraUnaEcuacionLineal(listaOutputs):
    pendiente = 231
    ordenadaAlOrigen = 89
    funcionLineal = lambda x : pendiente * x + ordenadaAlOrigen

    cantidadDeDatos = 100
    datosX = []
    datosY = []
    for i in range(cantidadDeDatos):
        datosX.append(i)
        datosY.append(funcionLineal(i))

    phi0 = lambda x : numpy.ones(cantidadDeDatos)
    phi1 = lambda x : x

    funcionesPhi = [phi0, phi1]
    constantes = CuadradosMinimos.MinimosCuadrados(funcionesPhi, datosX, datosY)

    listaOutputs.append(Output(CompararFloat(ordenadaAlOrigen, constantes[0]), "Tienen la misma ordenada al origen"))
    listaOutputs.append(Output(CompararFloat(pendiente, constantes[1]), "Tienen la misma pendiente"))

    errorCuadraticoMedio = CuadradosMinimos.ErrorCuadraticoMedio(funcionesPhi, constantes, datosX, datosY)
    
    listaOutputs.append(Output(errorCuadraticoMedio < 0.0001, "Tiene un error cuadratico medio casi nulo"))

def PruebaFuncionCosenoTieneCuadradosMinimosPerfectosContraUnaEcuacionDeCoseno(listaOutputs):
    primeraFrecuencia = 39
    primeraConstate = 3
    segundaFrecuencia = 67
    segundaConstante = -93.3
    funcionSinusoidal = lambda x : primeraConstate * numpy.cos(x * primeraFrecuencia) + segundaConstante * numpy.cos(x * segundaFrecuencia)

    cantidadDeDatos = 100
    datosX = []
    datosY = []
    for i in range(cantidadDeDatos):
        datosX.append(i)
        datosY.append(funcionSinusoidal(i))

    phi0 = lambda x, primeraFrecuencia = primeraFrecuencia : numpy.cos(numpy.multiply(x, primeraFrecuencia))
    phi1 = lambda x, segundaFrecuencia = segundaFrecuencia : numpy.cos(numpy.multiply(x, segundaFrecuencia))

    funcionesPhi = [phi0, phi1]
    constantes = CuadradosMinimos.MinimosCuadrados(funcionesPhi, datosX, datosY)

    listaOutputs.append(Output(CompararFloat(primeraConstate, constantes[0]), "Tienen la misma primera frecuencia"))
    listaOutputs.append(Output(CompararFloat(segundaConstante, constantes[1]), "Tienen la misma segunda frecuencia"))

    errorCuadraticoMedio = CuadradosMinimos.ErrorCuadraticoMedio(funcionesPhi, constantes, datosX, datosY)
    
    listaOutputs.append(Output(errorCuadraticoMedio < 0.0001, "Tiene un error cuadratico medio casi nulo"))

def PruebaFuncionesCosenoSenoTieneCuadradosMinimosPerfectosContraUnaPropuestaDeFuncionIgual(listaOutputs):
    primeraFrecuencia = 39
    primeraConstate = 3
    segundaFrecuencia = 67
    segundaConstante = -93.3
    funcionSinusoidal = lambda x : primeraConstate * numpy.cos(x * primeraFrecuencia) + segundaConstante * numpy.sin(x * segundaFrecuencia)

    cantidadDeDatos = 100
    datosX = []
    datosY = []
    for i in range(cantidadDeDatos):
        datosX.append(i)
        datosY.append(funcionSinusoidal(i))

    phi0 = lambda x, primeraFrecuencia = primeraFrecuencia : numpy.cos(numpy.multiply(x, primeraFrecuencia))
    phi1 = lambda x, segundaFrecuencia = segundaFrecuencia : numpy.sin(numpy.multiply(x, segundaFrecuencia))

    funcionesPhi = [phi0, phi1]
    constantes = CuadradosMinimos.MinimosCuadrados(funcionesPhi, datosX, datosY)

    listaOutputs.append(Output(CompararFloat(primeraConstate, constantes[0]), "Tienen la misma primera frecuencia"))
    listaOutputs.append(Output(CompararFloat(segundaConstante, constantes[1]), "Tienen la misma segunda frecuencia"))

    errorCuadraticoMedio = CuadradosMinimos.ErrorCuadraticoMedio(funcionesPhi, constantes, datosX, datosY)
    
    listaOutputs.append(Output(errorCuadraticoMedio < 0.0001, "Tiene un error cuadratico medio casi nulo"))

def FuncionAuxilear(frecuencias, constantes, valor):
    resultado = 0
    for i in range(len(frecuencias)):
        resultado += constantes[i] * numpy.cos(valor * frecuencias[i])
        resultado += constantes[i] * numpy.sin(valor * frecuencias[i])
    return resultado

def PruebaMuchasFuncionesDeCosenosYSenosTieneCuadradosMinimosPerfectosContraUnaPropuestaDeFuncionIgual(listaOutputs):
    frecuencias = [1, 4, 6, 8, 9, 43]
    constantes = [54.3, -12.3, 84.3, 23.4, -1, 4]
    funcionSinusoidal = lambda x, frecuencias = frecuencias, constantes = constantes: FuncionAuxilear(frecuencias, constantes, x)

    cantidadDeDatos = 100
    datosX = []
    datosY = []
    for i in range(cantidadDeDatos):
        datosX.append(i)
        datosY.append(funcionSinusoidal(i))

    funcionesPhi = []
    for frecuencia in frecuencias:
        funcionesPhi.append(lambda x, frecuencia = frecuencia: numpy.cos(numpy.multiply(x, frecuencia)))
        funcionesPhi.append(lambda x, frecuencia = frecuencia: numpy.sin(numpy.multiply(x, frecuencia)))

    vectorResultado = CuadradosMinimos.MinimosCuadrados(funcionesPhi, datosX, datosY)

    for i, constante in enumerate(constantes):
        listaOutputs.append(Output(CompararFloat(constante, vectorResultado[2 * i]), f"Tiene la misma frecuencia para el coseno {frecuencias[i]} con {vectorResultado[2 * i]}"))
        listaOutputs.append(Output(CompararFloat(constante, vectorResultado[2 * i + 1]), f"Tiene la misma frecuencia para el seno {frecuencias[i]}  con {vectorResultado[2 * i + 1]}"))

    errorCuadraticoMedio = CuadradosMinimos.ErrorCuadraticoMedio(funcionesPhi, vectorResultado, datosX, datosY)
    
    listaOutputs.append(Output(errorCuadraticoMedio < 0.0001, f"Tiene un error cuadratico medio casi nulo, de {errorCuadraticoMedio}"))

def MostrarPruebas(listaOutputs):
    for output in listaOutputs:
        print(output)

def Main():
    print("Pruebas: ")
    listaOutputs = []
    PruebaFuncionLinealTieneCuadradosMinimosPerfectosContraUnaEcuacionLineal(listaOutputs)
    PruebaFuncionCosenoTieneCuadradosMinimosPerfectosContraUnaEcuacionDeCoseno(listaOutputs)
    PruebaFuncionesCosenoSenoTieneCuadradosMinimosPerfectosContraUnaPropuestaDeFuncionIgual(listaOutputs)
    PruebaMuchasFuncionesDeCosenosYSenosTieneCuadradosMinimosPerfectosContraUnaPropuestaDeFuncionIgual(listaOutputs)
    MostrarPruebas(listaOutputs)


if __name__ == "__main__":
    Main()