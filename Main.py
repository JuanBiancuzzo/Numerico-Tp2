from numpy import genfromtxt, ndarray, float64
from Configuracion import caracterSeparador, lineasASaltear, columaAUsar, datosUnaHoraArchivo
from Plots import MostrarDatos

def LeerArchivo(nombreArchivo) -> ndarray:
    return genfromtxt(nombreArchivo, dtype = float64, delimiter = caracterSeparador, skip_header = lineasASaltear, usecols = columaAUsar)


def Main():
    lista = LeerArchivo(datosUnaHoraArchivo)
    MostrarDatos(lista, 1, "Datos en bruto", "Horas", "Altura")

if __name__ == "__main__":
    Main()