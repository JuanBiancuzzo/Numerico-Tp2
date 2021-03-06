from numpy import float64, dot, ndarray, linalg, array, multiply, subtract, add, arctan, cos
from math import sqrt

def MinimosCuadrados(funcionesPhi, datosX, datosY):
    matriz = CalculoDeLaMatriz(funcionesPhi, datosX)
    vector = CalculoDeFunciones(funcionesPhi, datosX, datosY)
    return ResolucionDeEcuacionesLineares(matriz, vector)

def ResolucionDeEcuacionesLineares(matriz, vector):
    return linalg.solve(matriz, vector)

def ErrorCuadraticoMedio(funcionesPhi, pesos, datosX : ndarray, datosY : ndarray) -> float:
    cantidadDeDatos = len(datosX)
    datosProcesados = FuncionEstrella(funcionesPhi, pesos, datosX)
    diferencia = subtract(datosY, datosProcesados)
    return sqrt(dot(diferencia, diferencia) / cantidadDeDatos)

def FuncionEstrella(funcionesPhi, pesos, datosX) -> ndarray:
    datosProcesados = array([])
    for i, funcionPhi in enumerate(funcionesPhi):
        resultado = multiply(funcionPhi(datosX), pesos[i])
        datosProcesados = resultado if datosProcesados.size == 0 else add(datosProcesados, resultado) 
    return datosProcesados

def CalculoDeAmplitudYFase(amplitudCoseno, amplitudSeno):
    fase = arctan(-amplitudSeno/amplitudCoseno)
    amplitud = amplitudCoseno/cos(fase)

    return fase, amplitud

def CalculoDeLaMatriz(funcionesPhi, datosX):
    matriz = []
    for i, funcionF in enumerate(funcionesPhi):
        fila = []
        resultadoF = funcionF(datosX)
        for j, funcionG in enumerate(funcionesPhi):
            resultadoG = funcionG(datosX)
            resultado = matriz[j][i] if j < i else ProductoInterno(resultadoF, resultadoG)
            fila.append(resultado)
        matriz.append(fila) 
    return matriz

def CalculoDeFunciones(funcionesPhi, datosX, datosY):
    vector = []
    for funcionPhi in funcionesPhi:
        resultado = ProductoInterno(funcionPhi(datosX), datosY)
        vector.append(resultado)
    return vector

def ProductoInterno(funcionF : ndarray, funcionG : ndarray) -> float64:
    return dot(funcionF, funcionG)
