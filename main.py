# Punto de entrada: lee el archivo, ejecuta las reglas y muestra el resultado
import sys
import lexer
import parser
import interpreter
import analyzer


# separa la parte de las reglas de la parte del estado (State:)
def separar_entrada(texto):
    lineas = texto.split("\n")
    lineas_reglas = []
    lineas_estado = []
    en_estado = False
    for linea in lineas:
        if linea.strip() == "State:":
            en_estado = True
            continue
        if en_estado:
            lineas_estado.append(linea)
        else:
            lineas_reglas.append(linea)
    return "\n".join(lineas_reglas), lineas_estado


# lee las variables (id = numero) y los hechos activos (id) del estado inicial
def leer_estado(lineas):
    variables = {}
    hechos = set()
    for linea in lineas:
        linea = linea.strip()
        if linea == "":
            continue
        if "=" in linea:
            partes = linea.split("=")
            nombre = partes[0].strip()
            valor = partes[1].strip()
            variables[nombre] = int(valor)
        else:
            hechos.add(linea)
    return variables, hechos


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py archivo.txt")
        return

    archivo = open(sys.argv[1], "r")
    texto = archivo.read()
    archivo.close()

    texto_reglas, lineas_estado = separar_entrada(texto)
    variables, hechos = leer_estado(lineas_estado)

    tokens = lexer.tokenize(texto_reglas)
    ast = parser.parse(tokens)

    activados = interpreter.ejecutar(ast, variables, hechos)

    # salida: los hechos activados, en orden alfabetico
    if len(activados) == 0:
        print("(no output)")
    else:
        for hecho in sorted(activados):
            print(hecho)

    # mensajes del analisis estatico
    mensajes = analyzer.analizar(ast, variables, hechos)
    for m in mensajes:
        print(m)


main()
