from csv import writer
from numpy import genfromtxt, ndarray, float64
from Configuracion import caracterSeparador, lineasASaltear, columaAUsar

def LeerArchivo(nombreArchivo) -> ndarray:
    return genfromtxt(nombreArchivo, dtype = float64, delimiter = caracterSeparador, skip_header = lineasASaltear, usecols = columaAUsar)

def GuardarCSV(nombreArchivo, valores, nombresDeValores):
    with open(nombreArchivo, 'w', newline='') as f:
        escritor = writer(f)
        escritor.writerow(nombresDeValores)
        for valor in valores:
            escritor.writerow(valor)


