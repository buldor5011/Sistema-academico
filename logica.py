# Base de datos estatica
ESTUDIANTES = {

"123" : "Alejandroo",
"456" : "Alejandroxx",
"789" : "Aleja Polilla",
"101" : "David Autista",
"202" : "Meridel la Iguana" ,
}

ASIGNATURAS = [
    "Logica Computacional",
    "Introduccion a la Ingenieria de Datos",
    "Cálculo Diferencial",
    "Algebra Lineal"
]


def buscar_estudiante(documento):
    return ESTUDIANTES.get(documento, None)

def validar_nota(valor):
    try:
        nota= float(valor)
        return 0 <= nota <= 5
    except ValueError:
        return False

def validar_asistencia(valor):
    try:
        asistencia= float(valor)
        return 0 <= asistencia <= 100
    except ValueError:
        return False
    




def calcular_estado(notas, asistencia):
    promedio = sum(notas) / len(notas)

    if asistencia <80:
        return promedio, "Reprobo por inasistencia", "red"

    elif promedio >=3.0:
        return promedio, "Aprobado", "green"
    else:
        return promedio, "Reprobo por nota", "red"
        
