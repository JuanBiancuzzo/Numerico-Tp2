from Configuracion import datosSeisMinutosArchivo, periodoConArchivoDeSeisMinutos
from Plots import MostrarDatos
from Transformacion import Transformada
from Utilidades import LeerArchivo, GuardarCSV
from numpy import float64

def CalcularPeriodo(periodoEnMinutos : float64):
    tipoDeDato = "min"

    if periodoEnMinutos / 60 > 1:
        tipoDeDato = "hora"
        periodoEnMinutos /= 60

        if periodoEnMinutos / 24 > 1:
            tipoDeDato = "dia"
            periodoEnMinutos /= 24

    return periodoEnMinutos, tipoDeDato

def Main():
    listaDeDatos = LeerArchivo(datosSeisMinutosArchivo)
    MostrarDatos(listaDeDatos, 1/(10 * 24), "Datos en bruto de enero", "Dias", "Altura")
    cantidadDeDatosEnMinutos = 31 * 24 * 10 * 6
    
    resultados = Transformada(listaDeDatos, 20)
    #MostrarDatos(resultados, "Datos de la transformada", "Frecuencias", "Importancia")

    informacionDeLosDatos = ["Orden", "Periodo", "Tipo de periodo"]
    datos = []
    for resultado in resultados:
        orden = int(resultado[1])
        periodo = cantidadDeDatosEnMinutos / orden
        periodo, tipoDePeriodo = CalcularPeriodo(periodo)

        print(f"Orden: {orden}, con un periodo de {periodo} {tipoDePeriodo}")

        datoIndividual = [orden, periodo, tipoDePeriodo]
        datos.append(datoIndividual)
    
    GuardarCSV(periodoConArchivoDeSeisMinutos, datos, informacionDeLosDatos)        
            

if __name__ == "__main__":
    Main()