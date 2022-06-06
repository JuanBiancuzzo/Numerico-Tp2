from numpy import genfromtxt, ndarray, float64
from Configuracion import caracterSeparador, lineasASaltear, columaAUsar, datosSeisMinutosArchivo
from Plots import MostrarDatos
from Transformacion import Transformada

def LeerArchivo(nombreArchivo) -> ndarray:
    return genfromtxt(nombreArchivo, dtype = float64, delimiter = caracterSeparador, skip_header = lineasASaltear, usecols = columaAUsar)

def Main():
    listaDeDatos = LeerArchivo(datosSeisMinutosArchivo)
    #MostrarDatos(lista, 1/(10 * 24), "Datos en bruto de enero", "Dias", "Altura")
    cantidadDeDatosEnMinutos = (len(listaDeDatos)) / 6
    
    resultados = Transformada(listaDeDatos, 20)
    for resultado in resultados:
        if resultado[1] != 0:
            frecuencia = cantidadDeDatosEnMinutos / resultado[1]
            print(f" {frecuencia / 60} horas")

if __name__ == "__main__":
    Main()